async function loadRequests() {

    const response = await fetch(
        "http://127.0.0.1:8000/requests"
    );

    const data = await response.json();

    const table =
        document.getElementById(
            "requestsTable"
        );

    table.innerHTML = "";

    data.forEach(item => {

        table.innerHTML += `
        <tr>
            <td>${item.request_id}</td>
            <td>${item.resource_type}</td>
            <td>${item.resource_name}</td>
            <td>${item.environment}</td>
            <td>${item.iac_tool}</td>
            <td>${item.status}</td>
        </tr>
        `;
    });
}

loadRequests();