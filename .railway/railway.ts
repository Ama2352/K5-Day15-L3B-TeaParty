import { defineRailway, github, project, service } from "railway/iac";

export default defineRailway(() => {
  const demo = service("teaparty-demo", {
    source: github("Ama2352/K5-Day15-L3B-TeaParty", { branch: "main" }),
  });

  return project("TeaParty", { resources: [demo] });
});
