$(document).ready(function () {

    $('#edit-bubble').click(function () {
        console.log("Inside edit bubble");
        const bubble_name = document.getElementById('bubble_name').value;
        console.log("Bubble name: " + bubble_name);
        const bubble_description = document.getElementById('bubble_description').value;
        const bubble_id = document.getElementById('bubble_id').innerHTML;
        console.log(bubble_id);
        console.log("Bubble description: " + bubble_description);

        $.ajax({
            type: 'POST',
            url: '/edit-bubble/' + bubble_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'bubble_name': bubble_name,
                'bubble_description': bubble_description
            }),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
    });

    $('#user-search').click(function () {
        const search_string = document.getElementById('search-form').value;
        const bubble_id = document.getElementById('bubble_id').innerHTML;

        $.ajax({
            type: 'GET',
            url: '/user-search/' + bubble_id + '/' + search_string,
            success: function(res) {
                users_table = document.getElementById('add-users-table');
                users_table.innerHTML = "";
                for (i = 0; i < res.response.length; i++) {
                    new_row = document.createElement('tr');
                    new_row.className = 'potential-user';
                    row_id = document.createElement('td');
                    row_id.innerHTML = res.response[i]['user_id'];
                    row_first_name = document.createElement('td');
                    row_first_name.innerHTML = res.response[i]['first_name'];
                    row_last_name = document.createElement('td');
                    row_last_name.innerHTML = res.response[i]['last_name'];
                    row_check_td = document.createElement('td');
                    row_check = document.createElement('input');
                    row_check.name = 'add-user-check';
                    row_check.type = 'checkbox';
                    row_check.id = res.response[i]['user_id'];
                    row_check_td.appendChild(row_check);
                    new_row.appendChild(row_id);
                    new_row.appendChild(row_first_name);
                    new_row.appendChild(row_last_name);
                    new_row.appendChild(row_check_td);
                    users_table.appendChild(new_row);
                }
            },
            error: function () {
                console.log("Error");
            }
        });
    });

    $('#add-users').click(function () {
        const bubble_id = document.getElementById('bubble_id').innerHTML;
        add_list = [];
        const to_add = document.querySelectorAll('input[name="add-user-check"]:checked');
        let user_ids = [];
        to_add.forEach((checkbox) => {
            user_ids.push(checkbox.id);
        });

        $.ajax({
            type: 'POST',
            url: '/add-users',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_ids': user_ids,
                'bubble_id': bubble_id
            }),
            success: function (res) {
                console.log(res.response);
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });

    });

    $('.remove').click(function () {
        const remove = $(this);
        const bubble_id = document.getElementById('bubble_id').innerHTML;

        var shouldRemove = confirm("Are you sure you want to remove this user?");
        if (shouldRemove == true) {
            $.ajax({
                type: 'POST',
                url: '/delete/' + bubble_id + '/' + remove.data('source'),
                success: function (res) {
                    console.log(res.response)
                    location.reload();
                },
                error: function () {
                    console.log('Error');
                }
            });
        }
        
    });

});