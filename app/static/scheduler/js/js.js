// link professors to courses
function addRow() {
    var selectedProfessor = $("#Professors").val();
    var selectedCourse = $("#selectedCourses").val();

    // Check if selectedCourse and selectedProfessor is not null
    if (selectedProfessor) {
        if (selectedCourse) {
            // Create a new row
            var newRow = $("<tr>").html(`
            <td>${selectedCourse}</td>
            <td>${selectedProfessor}</td>
            <td><button class='btn btn-danger' id='remove_linked_course'>Remove</button></td>
        `);

            // Append the row to the table
            $("#linkedcoursesTable tbody").append(newRow);
        }
    }
}
$(document).on("click", "#remove_linked_course", function () {
    $(this).closest("tr").remove();
});
// -----------------------------------------------------
function addRow_limit_prof() {
    let linked_courses_to_professors = [];
    // Get all rows in the table

    var selectedProfessor = $("#select_prof_for_limit").val();
    var selectedDay = $("#select_day_for_limit").val();
    var selectedTime = $("#select_time_for_limit").val();

    if (!(selectedProfessor == null)) {
        var newRow = $("<tr>").html(`
        <td>${selectedProfessor}</td>
        <td>${selectedDay}</td>
        <td>${selectedTime}</td>
        <td><button class='btn btn-danger' id='remove_limited_professor'>Remove</button></td>
    `);
    }

    // Append the row to the table
    $("#limited_professors tbody").append(newRow);
}
$(document).on("click", "#remove_limited_professor", function () {
    $(this).closest("tr").remove();
});
// -----------------------------------------------------
var coursesWithoutCondition = [];

$("#get-data-btn").click(function () {
    // Create a list to store selected courses
    let selected_courses = [];

    // Create a dictionary to store limited professors time
    let limited_professors = {};

    // Get all checkboxes
    let checkboxes = $(".checkboxes");

    // Get chromosomes
    let chromosomes = $("#chromosomes").val();

    
    // Get desired_generations
    let desired_generations = $("#desired_generations").val();
    

    // Get courses with out conditions
    var courses_with_out_conditions = coursesWithoutCondition.join("-");
    // let courses_with_out_conditions = $("#courses_with_out_conditions").val();


    // Loop through all checkboxes
    checkboxes.each(function () {
        // If checkbox is checked, add course to the list
        if ($(this).is(":checked")) {
            selected_courses.push($(this).val());
        }
    });

    // Get all rows in the table
    let limited_professors_rows = $("#limited_professors tbody tr");

    // Loop through all limited professors time
    limited_professors_rows.each(function () {
        // Get course and professor from the row
        let professor = $(this).find("td").eq(0).text();
        let day = $(this).find("td").eq(1).text();
        let time = $(this).find("td").eq(2).text();

        if (!(`|${professor}|` in limited_professors)) {
            limited_professors[`|${professor}|`] = [[day, time]];
        } else {
            limited_professors[`|${professor}|`].push([day, time]);
        }
    });

    function postRequest() {
        preLoader()
        $.ajax({
            url: "http://127.0.0.1:8000/schedule/",
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
            },
            data: JSON.stringify({
                selected_courses: selected_courses,
                limited_professors: limited_professors,
                chromosomes: chromosomes,
                courses_with_out_conditions: courses_with_out_conditions,
                cpu_protector: cpu_protector,
                desired_generations: desired_generations
            }),
            success: function (data) {
                if (data.status == "ok") {
                    window.location.href = "http://127.0.0.1:8000/show_schedule/";
                }
            },
        });
    }

    // Get Cpu Protector Option
    let cpu_protector_input = $("#cpu_protector");
    let cpu_protector = "off";
    if($(cpu_protector_input).is(":checked")) {
        cpu_protector = "on";
        postRequest()
    } else {
        if(confirm("It's Better To Enable CPU Protector, Are You Sure That You Want to Continue Without This Option?")) {
            cpu_protector = "off";
            postRequest()
        }
    }


});

// -----------------------------------------------------
function preLoader() {
    $(document).ready(function () {
            // Create an overlay div
            $("body").append('<div id="overlay"></div>');
            $("#overlay").css({
                position: "fixed",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
                "background-color": "rgba(0,0,0,0.5)",
                "z-index": 1000,
            });
    
            // Position the loader in the middle of the page
            $(".lds-facebook").removeClass("d-none");
            $(".lds-facebook").css({
                position: "fixed",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
                "z-index": 1001,
            });
    
            // Show the loader
            $(".lds-facebook").show();
        });
}
// ----------------------------------------------------------
$(document).ready(function () {
    // When the button is clicked
    $("#checkAll").click(function () {
        var isChecked = $(this).is(":checked");
        // Set 'checked' property to true for all checkboxes
        $(".checkboxes").prop("checked", isChecked);
    });
});
// ----------------------------------------------------------
var a = document.getElementById("courses-without-conditions");
var cwd = document.getElementsByClassName("courses-without-cond")[0];

a.addEventListener("change", function () {
    var value = this.value;
    var lastOfValue = value.split("_").slice(-1)[0];
    if (value === "") return;
    if (coursesWithoutCondition.indexOf(value) === -1)
        coursesWithoutCondition.push(value);
    cwd.textContent = "";
    coursesWithoutCondition.map((course) => {
        var child = document.createElement("div");
        child.className = "courses-without-cond--item";
        child.textContent = course;
        child.addEventListener("click", () => {
            var index = coursesWithoutCondition.indexOf(course);
            coursesWithoutCondition.splice(index, 1);
            rebuild();
        });
        cwd.appendChild(child);
    });
});

function rebuild() {
    cwd.textContent = "";
    coursesWithoutCondition.map((course) => {
        var child = document.createElement("div");
        child.className = "courses-without-cond--item";
        child.textContent = course;
        child.addEventListener("click", () => {
            var index = coursesWithoutCondition.indexOf(course);
            coursesWithoutCondition.splice(index, 1);
            rebuild();
        });
        cwd.appendChild(child);
    });
}
// ----------------------------------------------------------
