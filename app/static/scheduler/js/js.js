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

    var selectedProfessor = $('#select_prof_for_limit').val();
    var selectedDay = $('#select_day_for_limit').val();
    var selectedTime = $('#select_time_for_limit').val();

    if (!(selectedProfessor == null)){
        var newRow = $('<tr>').html(`
        <td>${selectedProfessor}</td>
        <td>${selectedDay}</td>
        <td>${selectedTime}</td>
        <td><button class='btn btn-danger' id='remove_limited_professor'>Remove</button></td>
    `);
    }

    // Append the row to the table
    $('#limited_professors tbody').append(newRow);

}
$(document).on('click', '#remove_limited_professor', function () {
    $(this).closest('tr').remove();
});
// -----------------------------------------------------
$('#get-data-btn').click(function () {
    // Create a list to store selected courses
    let selected_courses = [];

    // Create a dictionary to store limited professors time
    let limited_professors = {};

    // Get all checkboxes
    let checkboxes = $('.form-check-input');

    // Get chromosomes
    let chromosomes = $("#chromosomes").val();

    // Get courses with out conditions
    let courses_with_out_conditions = $("#courses_with_out_conditions").val();
    
    // Get penalty chromosomes number
    let penalty_chromosomes = $("#penalty_chromosomes").val();


    // Loop through all checkboxes
    checkboxes.each(function () {
        // If checkbox is checked, add course to the list
        if ($(this).is(':checked')) {
            selected_courses.push($(this).val());
        }
    });

    // Get all rows in the table
    let limited_professors_rows = $('#limited_professors tbody tr');

    // Loop through all limited professors time
    limited_professors_rows.each(function () {
        // Get course and professor from the row
        let professor = $(this).find('td').eq(0).text();
        let day = $(this).find('td').eq(1).text();
        let time = $(this).find('td').eq(2).text();

        if (!(`|${professor}|` in limited_professors)) {
            limited_professors[`|${professor}|`] = [[day, time]];
        } else {
            limited_professors[`|${professor}|`].push([day, time]);
        }
    });

   
    $.ajax({
        url: 'http://127.0.0.1:8000/schedule/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
        },
        data: JSON.stringify({
            selected_courses: selected_courses,
            limited_professors: limited_professors,
            chromosomes: chromosomes,
            penalty_chromosomes:penalty_chromosomes,
            courses_with_out_conditions:courses_with_out_conditions
        }),
        success: function (data) {
            if (data.status == "ok") {
                window.location.href = "http://127.0.0.1:8000/show_schedule/";
            }
        }
    });
    
});

// -----------------------------------------------------
$(document).ready(function () {
    $('#get-data-btn').click(function () {
        // Create an overlay div
        $('body').append('<div id="overlay"></div>');
        $('#overlay').css({
            'position': 'fixed',
            'top': 0,
            'left': 0,
            'width': '100%',
            'height': '100%',
            'background-color': 'rgba(0,0,0,0.5)',
            'z-index': 1000
        });

        // Position the loader in the middle of the page
        $(".lds-facebook").removeClass("d-none");
        $('.lds-facebook').css({
            'position': 'fixed',
            'top': '50%',
            'left': '50%',
            'transform': 'translate(-50%, -50%)',
            'z-index': 1001
        });

        // Show the loader
        $('.lds-facebook').show();
    });
});


// --------------------------------------
document.getElementById('chromosomes').addEventListener('input', function () {
    if (this.value > 100000000) {
        alert('chromosomes cannot exceed 100000000');
        this.value = 100000000;
    }
});
// --------------------------------------
document.getElementById('penalty_chromosomes').addEventListener('input', function () {
    if (this.value > 100000000) {
        alert('penalty_chromosomes cannot exceed 100000000');
        this.value = 100000000;
    }
});
// ----------------------------------------------------------

$(document).ready(function () {
    // When the button is clicked
    $("#checkAll").click(function () {
        // Set 'checked' property to true for all checkboxes
        $('.form-check-input').prop('checked', true);
    });
});
// ----------------------------------------------------------