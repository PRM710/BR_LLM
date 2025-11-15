import React, { useState } from "react";
import axios from "axios";
import "./QASystem.css";

export default function QASystem() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/ask", {
        question: question,
      });

      setAnswer(res.data.answer);
    } catch (err) {
      setAnswer("Error: Backend not running!");
    }

    setLoading(false);
  };

  return (
    <div className="qa-container">
      <h1 className="qa-title">Ambedkar Q&A System</h1>

      <textarea
        className="qa-input"
        rows="3"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask any question from the speech..."
      />

      <button className="qa-button" onClick={ask}>
        Ask
      </button>

      {loading && <p className="qa-loading">Thinking...</p>}

      {answer && (
        <div className="qa-answer">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
