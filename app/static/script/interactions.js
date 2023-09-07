$(document).ready(function () {
    // example: https://getbootstrap.com/docs/4.2/components/modal/
    // show modal
    

    $('#task-modal').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget) // Button that triggered the modal
        const taskID = button.data('source') // Extract info from data-* attributes
        const content = button.data('content') // Extract info from data-* attributes

        var now = new Date();
        var todayUTC = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
        $('#id1').val(todayUTC.toISOString().slice(0, 10));

        const modal = $(this)
        if (taskID === 'New Interactions') {
            modal.find('.modal-title').text(taskID)
            $('#task-form-display').removeAttr('taskID')
        } else {
            modal.find('.modal-title').text('Edit Interaction ' + taskID)
            $('#task-form-display').attr('taskID', taskID)
        }

        if (content) {
            modal.find('.form-control').val(content);
        } else {
            modal.find('.form-control').val('');
        }
    })

    $('#submit-task').click(function (e) {
        const tID = $('#task-form-display').attr('taskID');
        console.log($('#task-modal').find('.form-control').val());
        const button = $(e.currentTarget);
        const user_id = button.data('source');

        $.ajax({
            type: 'POST',
            url:  tID ? '/edit_interaction/' + tID : '/create_interaction/'+user_id,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'description1': $('#id1').val(),
                'description2': $('#id2').val(),
                'description3': $('#id3').val(),
                'description4': $('#id4').val()
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

    $('.remove').click(function () {
        const remove = $(this)
 
        $.ajax({
            type: 'POST',
            url: '/delete_interaction/' + remove.data('source'),
            success: function (res) {
                console.log(res.response)
                location.reload();
            },
            error: function () {
                console.log('Error');
            }
        });
        
    });


    $('#table_search').click(function () {
        const search_string = document.getElementById('table').value;
        $.ajax({
            type: 'GET',
            url: '/search_interaction'+'/'+search_string ,
            // data: JSON.stringify({
            //     'search1': $('#mysearch').val()}),
            success: function (res) {
                console.log(res.response)
                window.location.href = '/search_interaction/'+search_string;
            },
            error: function () {
                console.log('Error');
            }
        });
        
    });

    $('#date_search').click(function (e) {
        const input = document.getElementById('date').value;
        const button = $(e.currentTarget);
        const user_id = button.data('source');
        
        console.log(input)
        $.ajax({
            type: 'GET',
            url:  '/interactions/' + user_id+'/search_date/'+input,
            // data: JSON.stringify({
            //     'search1': $('#mysearch').val()}),
            success: function (res) {
                console.log(res.response)
                window.location.href = '/interactions/' + user_id+'/search_date/'+input;
            },
            error: function () {
                console.log('Error');
            }
        });
       
    });



});
