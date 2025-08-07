const { exec } = require("child_process");

// backendディレクトリに移動してから起動
const cmd = "cd backend && uvicorn main:app --reload";

const proc = exec(cmd, { stdio: "inherit" });

proc.stdout && proc.stdout.pipe(process.stdout);
proc.stderr && proc.stderr.pipe(process.stderr);

proc.on("close", (code) => {
  process.exit(code);
});
