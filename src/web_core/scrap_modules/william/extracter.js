const william_odds = Array
    .prototype
    .slice
    .call(
        document
        .getElementsByClassName("betbutton__odds")
    )
    .map(
        function (match){return match.innerText}
    );
const william_names = Array
    .prototype
    .slice
    .call(
        document
        .getElementsByClassName("btmarket__content")
    )
    .map(
        function (match){return match.innerText}
    );

return {"odds": william_odds, "names": william_names};