"""Streamlit components shared by the interview-prep pages."""
from __future__ import annotations

import secrets
from typing import Callable, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from grading.llm import api_available, grade_answer
from grading.question import Question, combine_scores
from progress import db

PALETTE = ["#2E6FD8", "#E07A1F", "#2A9D6F", "#B8443A", "#7A5CC2"]


def plot_chart(spec: dict) -> go.Figure:
    """Render a chart spec from :mod:`grading.question`."""
    fig = go.Figure()
    if spec["type"] == "line":
        for i, (name, ys) in enumerate(spec["series"].items()):
            fig.add_trace(go.Scatter(x=spec["x"], y=ys, mode="lines", name=name,
                                     line=dict(color=PALETTE[i % len(PALETTE)], width=2,
                                               dash="solid" if i == 0 else "dash")))
        if spec.get("vline") is not None:
            fig.add_vline(x=spec["vline"], line=dict(color="#888", dash="dot"),
                          annotation_text=spec.get("vline_label", ""), annotation_position="top")
        fig.update_layout(xaxis_title=spec["xlabel"], yaxis_title=spec["ylabel"])
    elif spec["type"] == "bar":
        colors = [PALETTE[2] if v >= 0 else PALETTE[3] for v in spec["values"]]
        fig.add_trace(go.Bar(x=spec["labels"], y=spec["values"], marker_color=colors))
        fig.update_layout(yaxis_title=spec["ylabel"])
    fig.update_layout(title=spec["title"], height=320, margin=dict(l=40, r=20, t=50, b=40),
                      legend=dict(orientation="h", y=-0.25), template="plotly_white")
    return fig


def new_seed() -> int:
    return secrets.randbelow(2**31 - 1)


def question_page(key: str, section: str, subsections: dict[str, tuple[str, Callable]],
                  review_pool: Optional[Callable[[int, int], Question]] = None,
                  locked: Optional[dict[str, str]] = None) -> None:
    """Full question workflow: pick, answer, submit, reveal, mark, log.

    ``subsections`` maps code -> (title, generator(seed, difficulty)).
    ``locked`` maps code -> reason for subsections not yet unlocked.
    """
    locked = locked or {}
    ss = st.session_state
    c1, c2, c3 = st.columns([3, 1.3, 1.2])
    labels = [f"{k}  {v[0]}" + ("  (locked)" if k in locked else "") for k, v in subsections.items()]
    if review_pool is not None:
        labels.append("Mixed review (weakest topics)")
    choice = c1.selectbox("Section", labels, key=f"{key}_sub")
    diff = c2.radio("Difficulty", [1, 2, 3], horizontal=True, key=f"{key}_diff")
    c3.write("")
    new = c3.button("New question", type="primary", key=f"{key}_new", use_container_width=True)

    code = choice.split()[0]
    if code in locked:
        st.info(locked[code])
        return
    qkey = f"{key}_q"
    if new or qkey not in ss or ss.get(f"{key}_qmeta") != (choice, diff):
        seed = new_seed()
        if choice.startswith("Mixed"):
            q = review_pool(seed, diff)
        else:
            q = subsections[code][1](seed, diff)
        ss[qkey] = q
        ss[f"{key}_qmeta"] = (choice, diff)
        ss[f"{key}_submitted"] = False
        ss[f"{key}_result"] = None
        ss[f"{key}_logged"] = False
    q: Question = ss[qkey]
    render_question(q, key)


def render_question(q: Question, key: str) -> None:
    ss = st.session_state
    st.caption(f"Topic: `{q.topic}`   Difficulty {q.difficulty}   Seed {q.seed}")
    st.markdown(q.prompt)
    answers: dict[int, object] = {}
    disabled = bool(ss.get(f"{key}_submitted"))
    for i, p in enumerate(q.parts):
        pk = f"{key}_{q.qid}_p{i}"
        if p.kind == "mcq":
            sel = st.radio(p.label, p.options, index=None, key=pk, disabled=disabled)
            answers[i] = None if sel is None else p.options.index(sel)
        elif p.kind == "numeric":
            answers[i] = st.number_input(f"{p.label}", value=None, format="%.4f", key=pk, disabled=disabled)
        elif p.kind == "sign_table":
            st.markdown(f"**{p.label}**")
            cols = st.columns(len(p.rows))
            ans = {}
            for c, r in zip(cols, p.rows):
                ans[r] = c.radio(r, ["+", "-", "0"], index=None, key=f"{pk}_{r}", disabled=disabled)
            answers[i] = ans
    free = ""
    if q.free_text_prompt:
        free = st.text_area(q.free_text_prompt, key=f"{key}_{q.qid}_free", height=140, disabled=disabled)

    if not ss.get(f"{key}_submitted"):
        if st.button("Submit", key=f"{key}_{q.qid}_submit", type="primary"):
            auto = q.auto_score(answers)
            graded = None
            if free.strip() and api_available():
                with st.spinner("Claude is marking your answer..."):
                    graded = grade_answer(q.prompt + "\n\n" + (q.free_text_prompt or ""), free, q.facts,
                                          q.rubric, q.model_answer)
            ss[f"{key}_submitted"] = True
            ss[f"{key}_result"] = {"answers": answers, "auto": auto, "graded": graded, "free": free}
            st.rerun()
        return
    _reveal(q, key)


def _reveal(q: Question, key: str) -> None:
    ss = st.session_state
    res = ss[f"{key}_result"]
    answers, auto, graded, free = res["answers"], res["auto"], res["graded"], res["free"]
    st.divider()
    st.subheader("1. Correct answer")
    for i, p in enumerate(q.parts):
        mark = p.mark(answers.get(i))
        icon = "✅" if mark == 1 else ("🟡" if mark > 0 else "❌")
        if p.kind == "sign_table":
            df = pd.DataFrame({
                "Greek": p.rows,
                "Your sign": [answers.get(i, {}).get(r) or "-" for r in p.rows],
                "Engine sign": ["/".join(p.correct[r]) if isinstance(p.correct[r], list) else p.correct[r] for r in p.rows],
            })
            df["OK"] = [("✅" if (df["Your sign"][j] in p.correct[r] if isinstance(p.correct[r], list)
                                  else df["Your sign"][j] == p.correct[r]) else "❌") for j, r in enumerate(p.rows)]
            st.markdown(f"{icon} **{p.label}** ({mark*100:.0f}%)")
            st.dataframe(df, hide_index=True, use_container_width=True)
        else:
            yours = answers.get(i)
            if p.kind == "mcq" and yours is not None:
                yours = p.options[yours]
            st.markdown(f"{icon} **{p.label}**: {p.correct_display()}  \n<small>Your answer: {yours}</small>",
                        unsafe_allow_html=True)
    for t in q.tables:
        st.markdown(f"**{t['title']}**")
        st.dataframe(pd.DataFrame(t["rows"], columns=t["columns"]), hide_index=True, use_container_width=True)

    st.subheader("2. Model answer (engine)")
    st.markdown(q.model_answer)

    if q.charts:
        st.subheader("3. Charts")
        cols = st.columns(min(len(q.charts), 2))
        for j, spec in enumerate(q.charts):
            cols[j % len(cols)].plotly_chart(plot_chart(spec), use_container_width=True,
                                             key=f"{key}_{q.qid}_chart{j}")

    st.subheader("4. Feedback on your written answer")
    llm_score = None
    if not q.free_text_prompt:
        st.caption("No written part for this question.")
    elif not free.strip():
        st.caption("You left the written part blank.")
    elif graded and "error" not in graded:
        llm_score = float(graded["score"])
        st.metric("Claude's mark", f"{graded['score']}/10")
        c1, c2, c3 = st.columns(3)
        c1.markdown("**Got right**\n" + "\n".join(f"- {x}" for x in graded["correct_points"]) if graded["correct_points"] else "**Got right**\n- (none)")
        c2.markdown("**Missed**\n" + "\n".join(f"- {x}" for x in graded["missed_points"]) if graded["missed_points"] else "**Missed**\n- (none)")
        c3.markdown("**Errors**\n" + "\n".join(f"- {x}" for x in graded["errors"]) if graded["errors"] else "**Errors**\n- (none)")
        with st.expander("Claude's model answer (uses engine numbers only)"):
            st.markdown(graded["model_answer"])
        if graded.get("cached"):
            st.caption("Cached marking.")
    else:
        if graded and "error" in graded:
            st.warning(f"Marking failed: {graded['error']}. Self-mark instead.")
        else:
            st.info("No ANTHROPIC_API_KEY set: compare with the engine model answer and self-mark.")
        llm_score = float(st.slider("Self-mark your written answer", 0, 10, 5, key=f"{key}_{q.qid}_self"))

    final = combine_scores(auto, llm_score)
    st.metric("Overall score", f"{final:.1f}/10")
    needs_self = q.free_text_prompt and free.strip() and not (graded and "error" not in graded)
    if not ss.get(f"{key}_logged"):
        if needs_self:
            if st.button("Save result", key=f"{key}_{q.qid}_save"):
                _log(q, key, auto, llm_score, final, res)
                st.rerun()
        else:
            _log(q, key, auto, llm_score, final, res)
    if ss.get(f"{key}_logged"):
        st.caption("Saved to your progress (spaced repetition updated). Press **New question** for the next one.")


def _log(q: Question, key: str, auto, llm, final, res) -> None:
    db.log_attempt(q.section, q.subsection, q.topic, q.difficulty, q.qid, final, auto, llm,
                   answer={"parts": res["answers"], "free": res["free"]}, feedback=res["graded"],
                   template=q.template, seed=q.seed)
    st.session_state[f"{key}_logged"] = True
