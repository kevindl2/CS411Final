$(document).ready(function () {

    $('#submit-bubble').click(function () {
        console.log("Inside submit bubble");
        const user_id = document.getElementById('user_id').innerHTML;
        console.log(user_id);
        const bubble_name = document.getElementById('bubble_name').value;
        console.log("Bubble name: " + bubble_name);
        const bubble_description = document.getElementById('bubble_description').value;
        console.log("Bubble description: " + bubble_description);

        $.ajax({
            type: 'POST',
            url: '/create-bubble',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'user_id': user_id,
                'bubble_name': bubble_name,
                'bubble_description': bubble_description
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

});