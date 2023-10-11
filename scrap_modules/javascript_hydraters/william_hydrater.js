window.scroll(0, 100000)


setTimeout(() => {
    elems = Q.getAll(".comp-container");

    for (let element of [...elems]){
        if (element.get("h3").innerText.endsWith("(Dobles)")){
            element.remove();
        }
    }
}
,1000)

