function taskAction(uri) {
    fetch(uri, {method: "GET"})
    .then((response) => response.text())
    .then((data) => alert(data))
    .catch((err) => alert(err));
}
