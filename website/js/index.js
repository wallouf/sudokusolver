/*global SudokuSolver _config*/

var SudokuSolver = window.SudokuSolver || {};
SudokuSolver.map = SudokuSolver.map || {};

var payloadToken = {};

(function homeScopeWrapper($) {
    var authToken;
    SudokuSolver.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = 'login.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = 'login.html';
    });
    
    function resetSolution() {
        $("#sudokuResult").addClass("d-none");
        $("#sudokuUploader").removeClass("d-none");
    }
    
    function requestSolution(picture) {

        var input = document.getElementById('sudokuPicture');
        if (!input) {
            alert("Couldn't find the fileinput element.");
        } else if (!input.files) {
            alert("This browser doesn't seem to support the `files` property of file inputs.");
        } else if (!input.files[0]) {
            alert("Please select a file before clicking 'Load'");               
        } else {
            var file = input.files[0];

            resizeAndUploadFile(file);
        }

        // $("#sudokuUploader").addClass("d-none");
        // $("#sudokuResult").removeClass("d-none");


        // $.ajax({
        //     method: 'POST',
        //     url: _config.api.invokeUrl + '/ride',
        //     headers: {
        //         Authorization: authToken
        //     },
        //     data: picture,
        //     contentType: 'application/json',
        //     success: completeRequest,
        //     error: function ajaxError(jqXHR, textStatus, errorThrown) {
        //         console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
        //         console.error('Response: ', jqXHR.responseText);
        //         alert('An error occured when requesting your unicorn:\n' + jqXHR.responseText);
        //     }
        // });
    }

    function completeRequest(result) {

    }

    function parseJwt (token) {
        var base64Url = token.split('.')[1];
        var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
        }).join(''));

        return JSON.parse(jsonPayload);
    };

    // Register click handler for #request button
    $(function onDocReady() {

        $('#sudokuPictureBtn').click(function() {
            requestSolution("");
        });

        $('#sudokuResetBtn').click(function() {
            resetSolution("");
        });

        $('#logoutBtn').click(function() {
            SudokuSolver.signOut();
            
            window.location = "login.html";
        });

        SudokuSolver.authToken.then(function updateAuthMessage(token) {
            if (token) {
                console.log(token);
                payloadToken = parseJwt(token);
                $("#userEmailInfo").text(payloadToken['cognito:username']);
            }
        });

    });

}(jQuery));
