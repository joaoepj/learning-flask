function fetch_obj() {
    fetch('/tester')
    .then(response => response.json())
    .then(function(data) {
        document.getElementById('elId')
        .innerHTML = data['jsonkey']        
    })
    
}


function fetch_api() {
    let data = { "command": "config-get", "service": ["dhcp4"] }
    fetch('http://200.19.145.141:7000', {
        method: 'POST',
        mode: "no-cors",
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(json => console.log(json))
    .then(function(data) {
            document.getElementById('elId')
                .innerHTML = JSON.stringify(data)
        })
}