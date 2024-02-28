function getSelectedCourses() {
    var selectedCourses = $('input[type="checkbox"]:checked').map(function () {
        return this.value;
    }).get();

    // Create options for the select input
    var selectInput = $('#selectedCourses');
    selectInput.empty(); // Clear existing options

    $.each(selectedCourses, function (index, course) {
        selectInput.append(new Option(course, course));
    });
}
// -----------------------------------------------------
// link professors to courses
function addRow() {
    var selectedProfessor = $('#Professors').val();
    var selectedCourse = $('#selectedCourses').val();

    // Check if selectedCourse and selectedProfessor is not null
    if (selectedProfessor) {
        if (selectedCourse) {
            // Create a new row
            var newRow = $('<tr>').html(`
            <td>${selectedCourse}</td>
            <td>${selectedProfessor}</td>
            <td><button class='btn btn-danger' id='remove_linked_course'>Remove</button></td>
        `);

            // Append the row to the table
            $('#linkedcoursesTable tbody').append(newRow);
        }
    }
}
$(document).on('click', '#remove_linked_course', function () {
    $(this).closest('tr').remove();
});
// -----------------------------------------------------
function addRow_limit_prof() {
    let linked_courses_to_professors = [];
    // Get all rows in the table
    let rows = $('#linkedcoursesTable tbody tr');

    // Loop through all linked_courses_to_professors
    rows.each(function () {
        // Get course and professor from the row
        let professor = $(this).find('td').eq(1).text();

        // Add course and professor to the dictionary
        linked_courses_to_professors.push(professor);
    });

    var selectedProfessor = $('#select_prof_for_limit').val();
    var selectedTime = $('#select_time_for_limit').val();

    if (linked_courses_to_professors.includes(selectedProfessor)) {
        // Create a new row
        var newRow = $('<tr>').html(`
            <td>${selectedProfessor}</td>
            <td>${selectedTime}</td>
            <td><button class='btn btn-danger' id='remove_limited_professor'>Remove</button></td>
        `);

        // Append the row to the table
        $('#limited_professors tbody').append(newRow);
    } else {
        alert(selectedProfessor + " has not Course.")
    }
}
$(document).on('click', '#remove_limited_professor', function () {
    $(this).closest('tr').remove();
});
// -----------------------------------------------------
$('#get-data-btn').click(function () {
    // Create a list to store selected courses
    let selected_courses = [];

    // Create a dictionary to store linked courses and professors
    let linked_courses_to_professors = {};

    // Create a dictionary to store limited professors time
    let limited_professors = {};

    // Get all checkboxes
    let checkboxes = $('.form-check-input');

    // Loop through all checkboxes
    checkboxes.each(function () {
        // If checkbox is checked, add course to the list
        if ($(this).is(':checked')) {
            selected_courses.push($(this).val());
        }
    });

    // Get all rows in the table
    let rows = $('#linkedcoursesTable tbody tr');

    // Loop through all linked_courses_to_professors
    rows.each(function () {
        // Get course and professor from the row
        let course = $(this).find('td').eq(0).text();
        let professor = $(this).find('td').eq(1).text();

        // Add course and professor to the dictionary
        linked_courses_to_professors[course] = professor;
    });


    // Get all rows in the table
    let limited_professors_rows = $('#limited_professors tbody tr');

    // Loop through all limited professors time
    limited_professors_rows.each(function () {
        // Get course and professor from the row
        let professor = $(this).find('td').eq(0).text();
        let time = $(this).find('td').eq(1).text();

        // Add course and professor to the dictionary
        // if (!(`|${professor}|` in limited_professors)) {
        //     limited_professors[`|${professor}|`] = [[time]];
        // } else {
        //     limited_professors[`|${professor}|`].push([time]);
        // }
        
        if (!(`|${professor}|` in limited_professors)) {
            limited_professors[`|${professor}|`] = [time];
        } else {
            limited_professors[`|${professor}|`].push(time);
        }
    });

    var all_courses_linked = selected_courses.every(function (course) {
        return linked_courses_to_professors.hasOwnProperty(course);
    });
    // console.log(limited_professors);
    // alert("sdjaldjk")
    if (all_courses_linked) {
        // Send data to server
        $.ajax({
            url: 'http://127.0.0.1:8000/schedule/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
            },
            data: JSON.stringify({
                selected_courses: selected_courses,
                linked_courses_to_professors: linked_courses_to_professors,
                limited_professors: limited_professors
            }),
            success: function (data) {
                if (data.status == "ok") {
                    window.location.href = "http://127.0.0.1:8000/show_schedule/";
                }
            }
        });
    } else {
        var not_linked_courses = selected_courses.filter(function (course) {
            return !linked_courses_to_professors.hasOwnProperty(course);
        });

        not_linked_courses.forEach(function (course) {
            alert(course + " is not linked to a professor");
        });
    }
});

// -----------------------------------------------------