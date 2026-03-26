let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

function displayTasks() {
    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach((task, index) => {
        const li=document.createElement("li");

        //Task text
        const span=document.createElement("span");
        span.textContent = task.text;

        if(task.completed) {
            span.classList.add("completed");
        }

        //Toggle complete
        span.addEventListener("click", () => {
            tasks[index].completed = !tasks[index].completed;
            saveTasks();
            displayTasks();
        })

       //Edit button
       const editbtn = document.createElement("button");
       editbtn.textContent = "edit";

       editbtn.onclick = (e) => {
        e.stopPropagation();

        const newText = prompt("Edit task:", task.text);

        if(newText !== null && newText.trim() !== ""){
            tasks[index].text = newText.trim();
            saveTasks();
            displayTasks();
        }
       }
        // Delete button
        const delBtn = document.createElement("button");
        delBtn.textContent = "delete";
        
        delBtn.onclick = (e) => {
            e.stopPropagation();
            tasks.splice(index, 1);
            saveTasks();
            displayTasks();
        }

        //Append elements
        li.appendChild(span);
        li.appendChild(editbtn);
        li.appendChild(delBtn);
        
        list.appendChild(li);

    });

}

function addTask() {
    const input = document.getElementById("taskInput");
    const text= input.value.trim();

    if(text === "") return;

    tasks.push({ text: text, completed: false});
    input.value="";

    saveTasks();
    displayTasks();
}

function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

//Initial load
displayTasks();