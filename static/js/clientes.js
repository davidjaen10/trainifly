'use strict';

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("clientes-list");
    const items = document.querySelectorAll(".cliente-item");

    if (!container || items.length === 0) {
        alert("No hay clientes para mostrar");
        return;
    }

    const table = document.createElement("table");
    table.setAttribute("border", "1");
    table.style.width = "100%";

    const thead = document.createElement("thead");
    thead.innerHTML = `
        <tr>
            <th>Nombre</th>
            <th>Email</th>
            <th>Usuario</th>
            <th>Plan</th>
            <th>Acciones</th>
        </tr>
    `;

    const tbody = document.createElement("tbody");

    items.forEach(item => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${item.dataset.nombre}</td>
            <td>${item.dataset.email}</td>
            <td>${item.dataset.usuario}</td>
            <td>${item.dataset.plan}</td>
            <td>
                <a href="/usuarios/editar/${item.dataset.id}/">
                    <button>Editar</button>
                </a>
                <a href="/usuarios/borrar/${item.dataset.id}/">
                    <button>Borrar</button>
                </a>
            </td>
        `;

        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);

    container.innerHTML = "";
    container.appendChild(table);

    // filtrar por nombre
    const filtro = document.getElementById("filtroClientes");

    if (filtro) {
        filtro.addEventListener("input", e => {
            const texto = e.target.value.toLowerCase();

            Array.from(tbody.querySelectorAll("tr")).forEach(row => {
                const nombre = row.children[0].textContent.toLowerCase();
                row.style.display = nombre.includes(texto) ? "" : "none";
            });
        });
    }

});
