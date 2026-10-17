"""Local-only HTTP API for the Danny AI OS development dashboard."""

from flask import Flask, jsonify

from app import graph

app = Flask(__name__)


@app.get("/api/status")
def status():
    return jsonify(
        {
            "status": "ok",
            "workflow": "Python + LangGraph manager demo is available.",
        }
    )


@app.post("/api/run")
def run_workflow():
    try:
        result = graph.invoke({"message": "Dashboard demo run"})
        message = result.get("message", "Workflow completed.")
        return jsonify({"status": "ok", "message": f"Workflow completed: {message}"})
    except Exception:
        app.logger.exception("Dashboard workflow failed")
        return jsonify({"status": "error", "error": "Workflow failed. Check the local server log."}), 500


if __name__ == "__main__":
    # Intentionally local-only; do not expose this development API to the public internet.
    app.run(host="127.0.0.1", port=8000, debug=False)
