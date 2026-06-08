async function loadInventory() {

    const response =
    await fetch(
        "/requests"
    );

    const data =
    await response.json();

    const table =
    document.getElementById(
        "inventoryTable"
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

loadInventory();