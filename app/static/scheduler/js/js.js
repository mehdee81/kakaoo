
function addRow() {
    const selectedProfessor = document.getElementById('Professors').value;
    const selectedCourse = document.getElementById('selectedCourses').value;

    // Create a new row
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${selectedCourse}</td>
        <td>${selectedProfessor}</td>
        <td><button class='btn btn-danger' onclick="removeRow(this)">Remove</button></td>
    `;

    // Append the row to the table
    document.getElementById('coursesTable').getElementsByTagName('tbody')[0].appendChild(newRow);
}

function removeRow(button) {
    const rowToRemove = button.closest('tr');
    rowToRemove.remove();
}
function getSelectedCourses() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    const selectedCourses = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Create options for the select input
    const selectInput = document.getElementById('selectedCourses');
    selectInput.innerHTML = ''; // Clear existing options

    selectedCourses.forEach(course => {
        const option = document.createElement('option');
        option.value = course;
        option.textContent = course;
        selectInput.appendChild(option);
    });
    

    


    document.getElementById('get-data-btn').addEventListener('click', function() {
        // Create a list to store selected courses
        let selected_courses = [];
    
        // Create a dictionary to store linked courses and professors
        let linked_courses_to_professors = {};
    
        // Get all checkboxes
        let checkboxes = document.querySelectorAll('.form-check-input');
    
        // Loop through all checkboxes
        for(let i = 0; i < checkboxes.length; i++) {
            // If checkbox is checked, add course to the list
            if(checkboxes[i].checked) {
                selected_courses.push(checkboxes[i].value);
            }
        }
    
        // Get all rows in the table
        let rows = document.querySelectorAll('#coursesTable tbody tr');
    
        // Loop through all rows
        for(let i = 0; i < rows.length; i++) {
            // Get course and professor from the row
            let course = rows[i].querySelectorAll('td')[0].innerText;
            let professor = rows[i].querySelectorAll('td')[1].innerText;
    
            // Add course and professor to the dictionary
            linked_courses_to_professors[course] = professor;
        }
    
        // Send data to server
        fetch('http://127.0.0.1:8000/schedule/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                selected_courses: selected_courses,
                linked_courses_to_professors: linked_courses_to_professors
            })
        });
    });
    
}