const { PythonShell } = require("python-shell");

// create a python shell that executes the python script
let pyshell = new PythonShell("python-Copy.py");

// send a message to the python script
pyshell.send("Hello from js");

// handle messages from the python script
pyshell.on("message", (message) => {
  // log the message
  console.log(message);
});

// handle the close event of the python shell
pyshell.on("close", (code) => {
  console.log(`Python shell exited with code ${code}`);
});
