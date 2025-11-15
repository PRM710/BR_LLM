import React, { useState } from "react";
import axios from "axios";

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
    <div style={{ maxWidth: "700px", margin: "40px auto", padding: "20px" }}>
      <h1 style={{ fontSize: "32px", marginBottom: "20px" }}>
        Ambedkar Q&A System
      </h1>

      <textarea
        rows="3"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask any question from the speech..."
        style={{
          width: "100%",
          padding: "12px",
          fontSize: "16px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          marginBottom: "12px"
        }}
      />

      <button
        onClick={ask}
        style={{
          padding: "12px 20px",
          fontSize: "16px",
          borderRadius: "6px",
          cursor: "pointer",
          background: "black",
          color: "white",
          marginBottom: "20px",
        }}
      >
        Ask
      </button>

      {loading && <p>Thinking...</p>}

      {answer && (
        <div
          style={{
            background: "#f0f0f0",
            padding: "15px",
            borderRadius: "6px",
            fontSize: "18px"
          }}
        >
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}
