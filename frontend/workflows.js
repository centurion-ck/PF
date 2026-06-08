async function loadWorkflows() {

    const response =
    await fetch(
        "http://127.0.0.1:8000/requests"
    );

    const data =
    await response.json();

    const table =
    document.getElementById(
        "workflowTable"
    );

    table.innerHTML = "";

    data.forEach(item => {

        if (
            item.status !== "APPROVED" &&
            item.status !== "TEAM_LEAD_APPROVED" &&
            item.status !== "MANAGER_APPROVED" &&
            item.status !== "SECURITY_APPROVAL"
        ) {
            return;
        }

        table.innerHTML += `
        <tr>
            <td>${item.request_id}</td>
            <td>${item.resource_type}</td>
            <td>${item.resource_name}</td>
            <td>${item.environment}</td>
            <td>${item.iac_tool}</td>
            <td>${item.status}</td>

            <td>
                <button
                onclick="runWorkflow('${item.request_id}')">
                    Run
                </button>
            </td>
        </tr>
        `;
    });
}

async function runWorkflow(requestId) {

    await fetch(
        "http://127.0.0.1:8000/run/" + requestId,
        {
            method: "POST"
        }
    );

    alert(
        "Workflow Started Successfully"
    );

    location.reload();
}

loadWorkflows();