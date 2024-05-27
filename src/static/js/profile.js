
let old = document.querySelectorAll('.my-card')[0].id
let old_element = document.querySelectorAll('.nav-item')[0]


let old_degree_chart = document.querySelectorAll("#degree div canvas")[0].id
let old_degree_element_chart = document.querySelectorAll("#degree .titles ul li")[0]

let old_time_chart = document.querySelectorAll("#times div canvas")[0].id
let old_time_element_chart = document.querySelectorAll("#times .titles ul li")[0]


var is_edit = false
let old_element_profile = document.getElementById("profile-img").cloneNode(true)
function show_views(element_id,element) {
    element.classList.add('active')
    document.getElementById(old).classList.add('hidden')
    document.getElementById(element_id).classList.remove('hidden')
    old_element.classList.remove('active')
    old = element_id
    old_element = element
    
}
function show_chart(element_id, element) {
    element.classList.add('active')
    document.getElementById(old_degree_chart).classList.add('hidden')
    document.getElementById(element_id).classList.remove('hidden')
    old_degree_element_chart.classList.remove('active')
    old_degree_chart = element_id
    old_degree_element_chart = element

}

function show_time_chart(element_id, element) {
    element.classList.add('active')
    document.getElementById(old_time_chart).classList.add('hidden')
    document.getElementById(element_id).classList.remove('hidden')
    old_time_element_chart.classList.remove('active')
    old_time_chart = element_id
    old_time_element_chart = element

}
function show_submit() {
    document.getElementById("edit-user-info").classList.toggle('hidden')
    if (is_edit) {
        document.getElementById("profile-img").innerHTML = old_element_profile.innerHTML
        is_edit = false
    } else {
        document.getElementById("user-img").innerHTML += `<span style="display: inline-block;width: 100%;text-align: center;background-color: #ffffff8c;font-size: 3rem;color: #124aa9;font-weight: bold;cursor: pointer;">+</span></div>`
        document.getElementById("profile-img").innerHTML += `<input type="file" name="img" id="image-input" onchange="previewImage(event)" hidden>`
        is_edit = true
    }
    
}
function previewImage(event) {
    var fileInput = event.target;
    var file = fileInput.files[0];
    var reader = new FileReader();

    reader.onload = function (e) {
        document.getElementById("user-img").style.backgroundImage = 'url(' + e.target.result + ')';
    };

    reader.readAsDataURL(file);
}