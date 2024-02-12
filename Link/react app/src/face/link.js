const spawner = require("child_process").spawn;

const data_to_py = "act";
console.log("data sent to python:", data_to_py);

//define subprocess files and data passed to it
const python_process = spawner("python", ["./python.py", data_to_py]);

//establish pipe between parent js and subprocess python
python_process.stdout.pipe(process.stdout);
