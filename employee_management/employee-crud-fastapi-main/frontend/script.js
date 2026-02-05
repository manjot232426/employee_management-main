const API_URL = "http://localhost:8000";

async function loadEmployees() {
    const res = await fetch(`${API_URL}/employees`);
    const data = await res.json();

    const tbody = document.querySelector("tbody");
    tbody.innerHTML = "";

    data.forEach(emp => {
        tbody.innerHTML += `
            <tr>
                <td>${emp.id}</td>
                <td>${emp.name}</td>
                <td>${emp.age}</td>
                <td>${emp.position}</td>
                <td>${emp.department}</td>
                <td>${emp.email}</td>
                <td>${emp.salary}</td>
                <td>${emp.experience}</td>
                <td>
                    <button class="edit-btn" onclick="editEmployee(${emp.id})">Edit</button>
                    <button class="delete-btn" onclick="deleteEmployee(${emp.id})">Delete</button>
                </td>
            </tr>
        `;
    });
}

async function submitForm() {
    const id = document.getElementById("emp-id").value;

    const empData = {
        name: document.getElementById("name").value,
        age: parseInt(document.getElementById("age").value),
        position: document.getElementById("position").value,
        department: document.getElementById("department").value,
        email: document.getElementById("email").value,
        salary: parseFloat(document.getElementById("salary").value),
        experience: parseInt(document.getElementById("experience").value)
    };

    if (!id) {
        await fetch(`${API_URL}/employees`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(empData)
        });
    } else {
        await fetch(`${API_URL}/employees/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(empData)
        });
    }

    resetForm();
    loadEmployees();
}

async function editEmployee(id) {
    const res = await fetch(`${API_URL}/employees/${id}`);
    const emp = await res.json();

    document.getElementById("emp-id").value = emp.id;
    document.getElementById("name").value = emp.name;
    document.getElementById("age").value = emp.age;
    document.getElementById("position").value = emp.position;
    document.getElementById("department").value = emp.department;
    document.getElementById("email").value = emp.email;
    document.getElementById("salary").value = emp.salary;
    document.getElementById("experience").value = emp.experience;
}

async function deleteEmployee(id) {
    await fetch(`${API_URL}/employees/${id}`, { method: "DELETE" });
    loadEmployees();
}

function resetForm() {
    document.getElementById("emp-id").value = "";
    document.getElementById("name").value = "";
    document.getElementById("age").value = "";
    document.getElementById("position").value = "";
    document.getElementById("department").value = "";
    document.getElementById("email").value = "";
    document.getElementById("salary").value = "";
    document.getElementById("experience").value = "";
}

loadEmployees();
