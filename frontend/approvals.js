async function loadApprovals() {

    const response =
    await fetch(
    "/requests"
    );

    const data =
    await response.json();

    const table =
    document.getElementById(
    "approvalTable"
    );

    data.forEach(item => {

        if(item.status !== "PENDING")
            return;

        const row = `
        <tr>

        <td>${item.request_id}</td>

        <td>${item.resource_name}</td>

        <td>${item.status}</td>

        <td>

        <button
        onclick="approve(
        '${item.request_id}'
        )">

        Approve

        </button>

        </td>

        </tr>
        `;

        table.innerHTML += row;

    });
}

async function approve(id){

    await fetch(

    "http://127.0.0.1:8000/approve/" + id,

    {
        method:"POST"
    }

    );

    location.reload();
}

loadApprovals();