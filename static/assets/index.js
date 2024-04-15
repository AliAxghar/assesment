function formSubmit(event) {
    event.preventDefault();
    var form = document.getElementById("formID");
    var clickedButtonValue = event.submitter.dataset.value;
    var formData = new FormData(form);
    formData.append('question', clickedButtonValue);
    fetch('/submit_form', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                response.json().then(res => {
                    if (res.question == 1) {
                        document.getElementById("data").innerHTML = res.data;
                    } else {
                        if (res.error) {
                            showMsg(res.msg);
                        } else {
                            document.getElementById("data").innerHTML = res.data;
                        }
                    }
                })
            } else {
                showMsg("Form submission failed");
                console.error('Form submission failed');
            }
        })
        .catch(error => {
            showMsg("Request failed: " + error);
            console.error('Request failed:', error);
        });
}

function showMsg(msg) {
    document.getElementById("msg").innerText = msg;
    setTimeout(() => {
        document.getElementById("msg").innerText = "";
        document.getElementById("clientForm").reset();
    }, 2000)
}