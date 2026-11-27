import { defineRailway, github, project, service } from "railway/iac";

export default defineRailway(() => {
  const demo = service("teaparty-demo", {
    source: github("Ama2352/K5-Day15-L3B-TeaParty", { branch: "main" }),
    start: 'python -m uvicorn --app-dir codebase web:app --host 0.0.0.0 --port "$PORT"',
    healthcheck: "/health",
    healthcheckTimeout: 30,
  });

  return project("TeaParty", { resources: [demo] });
});
