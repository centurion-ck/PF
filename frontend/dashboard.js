async function loadDashboard() {

    const response =
    await fetch(
    "http://127.0.0.1:8000/requests"
    );

    const data =
    await response.json();

    document.getElementById(
    "total"
    ).innerText = data.length;

    document.getElementById(
    "pending"
    ).innerText =
    data.filter(
        x => x.status === "PENDING"
    ).length;

    document.getElementById(
    "approved"
    ).innerText =
    data.filter(
        x => x.status === "APPROVED"
    ).length;

    document.getElementById(
    "success"
    ).innerText =
    data.filter(
        x => x.status === "SUCCESS"
    ).length;
}

loadDashboard();

async function loadDashboard() {

    const response = await fetch(
        "http://127.0.0.1:8000/requests"
    );

    const data = await response.json();

    document.getElementById("total").innerText =
        data.length;

    document.getElementById("pending").innerText =
        data.filter(x => x.status === "PENDING").length;

    document.getElementById("approved").innerText =
        data.filter(x => x.status === "APPROVED").length;

    document.getElementById("success").innerText =
        data.filter(x => x.status === "SUCCESS").length;

    document.getElementById("cloudformation").innerText =
        data.filter(x => x.iac_tool === "CloudFormation").length;

    document.getElementById("terraform").innerText =
        data.filter(x => x.iac_tool === "Terraform").length;
}

loadDashboard();