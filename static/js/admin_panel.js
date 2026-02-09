'use strict';

document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("admin-grid");
    if (!grid) return;

    const gridDiv = document.createElement("div");
    gridDiv.className = "grid";

    // boton de crear client
    const linkCreate = document.createElement("a");
    linkCreate.href = "/create_user/";
    linkCreate.className = "item-link";

    const cardCreate = document.createElement("div");
    cardCreate.className = "item";

    const iconCreate = document.createElement("i");
    iconCreate.className = "fas fa-user-plus";

    const textCreate = document.createElement("p");
    textCreate.textContent = "Crear Cliente";

    cardCreate.appendChild(iconCreate);
    cardCreate.appendChild(textCreate);
    linkCreate.appendChild(cardCreate);
    gridDiv.appendChild(linkCreate);

    //boton de lista clientes
    const linkList = document.createElement("a");
    linkList.href = URL_CLIENTES;
    linkList.className = "item-link";

    const cardList = document.createElement("div");
    cardList.className = "item";

    const iconList = document.createElement("i");
    iconList.className = "fas fa-users";

    const textList = document.createElement("p");
    textList.textContent = "Lista de Clientes";

    cardList.appendChild(iconList);
    cardList.appendChild(textList);
    linkList.appendChild(cardList);
    gridDiv.appendChild(linkList);

    grid.appendChild(gridDiv);
});
