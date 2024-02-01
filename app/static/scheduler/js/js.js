function getSelectedCourses() {
    var selectedCourses = $('input[type="checkbox"]:checked').map(function() {
        return this.value;
    }).get();

    // Create options for the select input
    var selectInput = $('#selectedCourses');
    selectInput.empty(); // Clear existing options

    $.each(selectedCourses, function(index, course) {
        selectInput.append(new Option(course, course));
    });
}

function addRow() {
    var selectedProfessor = $('#Professors').val();
    var selectedCourse = $('#selectedCourses').val();

    // Create a new row
    var newRow = $('<tr>').html(`
        <td>${selectedCourse}</td>
        <td>${selectedProfessor}</td>
        <td><button class='btn btn-danger'>Remove</button></td>
    `);

    // Append the row to the table
    $('#coursesTable tbody').append(newRow);
}
$(document).on('click', '.btn-danger', function() {
    $(this).closest('tr').remove();
});


$('#get-data-btn').click(function () {
    // Create a list to store selected courses
    let selected_courses = [];

    // Create a dictionary to store linked courses and professors
    let linked_courses_to_professors = {};

    // Get all checkboxes
    let checkboxes = $('.form-check-input');

    // Loop through all checkboxes
    checkboxes.each(function() {
        // If checkbox is checked, add course to the list
        if ($(this).is(':checked')) {
            selected_courses.push($(this).val());
        }
    });

    // Get all rows in the table
    let rows = $('#coursesTable tbody tr');

    // Loop through all rows
    rows.each(function() {
        // Get course and professor from the row
        let course = $(this).find('td').eq(0).text();
        let professor = $(this).find('td').eq(1).text();

        // Add course and professor to the dictionary
        linked_courses_to_professors[course] = professor;
    });

    var all_courses_linked = selected_courses.every(function (course) {
        return linked_courses_to_professors.hasOwnProperty(course);
    });

    if (all_courses_linked) {
        // Send data to server
        var currentUrl = window.location.href;
        $.ajax({
            url: currentUrl+'/schedule/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
            },
            data: JSON.stringify({
                selected_courses: selected_courses,
                linked_courses_to_professors: linked_courses_to_professors
            })
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
