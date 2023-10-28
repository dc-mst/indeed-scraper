function jobTitleLinkFormatter(value, row) {
    return `<a href="${row.Href}" target="_blank">${value}</a>`;
}

function checkAllRowsVisibleAndUpdateButton() {
    var anyChecked = false; // Assume no rows are hidden initially
    $('input[name="btSelectItem"]').each(function() {
        if ($(this).prop('checked')) {
            anyChecked = true;
            return false; // Exit the loop early if a checked checkbox is found
        }
    });

    var $showAllBtn = $('#showAllBtn');
    // If any row is hidden (any checkbox is checked)
    if (anyChecked) {
        $showAllBtn.show(); // Show the button
    } else {
        $showAllBtn.hide(); // Hide the button if there are no hidden rows
    }
}


$('#table').bootstrapTable({
    url: '/data',
    sortName: ['Timestamp', 'Source'],  // specify both fields in an array
    sortOrder: ['desc', 'asc'],          // specify the order for each field 
    pagination: true,
    search: true,
    filterControl: true,
    columns: [{
        checkbox: true,
    }, {
        field: 'Timestamp',
        title: 'Timestamp',
        sortPriority: 2         
    }, {
        field: 'Source',
        title: 'Source',
        sortPriority: 1,
        filterControl: 'select'
    }, {
        field: 'Job Title',
        title: 'Job Title',
        formatter: jobTitleLinkFormatter
    }, {
        field: 'Description',
        title: 'Description'
    }],
        onLoadSuccess: function(data) {
        // Loop through the data to check the Hidden value
        for (let i = 0; i < data.length; i++) {
            if (data[i].Hidden) { // If Hidden is true, hide the row
                const rowIndex = $('tr[data-index="' + i + '"]');
                rowIndex.find('input[name="btSelectItem"]').prop('checked', true);
                rowIndex.hide();
            }
        }
        checkAllRowsVisibleAndUpdateButton();
    }
});

function saveHiddenRowsState() {
    var hiddenRows = [];
    $('tr[data-index]').each(function() {
        var $row = $(this);
        var rowIndex = parseInt($row.data('index'));
        // Check if the checkbox is checked, not if the row is hidden
        if ($row.find('input[name="btSelectItem"]').prop('checked')) {
            hiddenRows.push(rowIndex);
        }
    });

    // The AJAX request to send hidden rows data to the server
    $.ajax({
        url: '/update_hidden_state',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ hiddenRows: hiddenRows }),
        success: function(response) {
            console.log(response.message);
        }
    });
}

$('#table').on('change', 'input[name="btSelectItem"]', function() {
    var $checkbox = $(this);
    var isChecked = $checkbox.prop('checked');
    var $row = $checkbox.closest('tr');
    var $tds = $row.find('td');

    if (isChecked) {
        $row.animate({
            height: 'toggle',
            opacity: 'toggle'
        }, 400, function() {
            $tds.css('background-color', ''); // Reset the background after animation completes
        });
    } else {
        $row.show();
        $row.css('opacity', '1');
        $tds.css('background-color', ''); // Reset the background when unchecked
    }
    saveHiddenRowsState();
    checkAllRowsVisibleAndUpdateButton();
});

$('#runScraperBtn').click(function() {
    // Show the progress bar
    $('#progressDiv').show();
    
    $.post("/run_scraper", function(data) {
        // Hide the progress bar
        $('#progressDiv').hide();
        
        // Show the Bootstrap Modal with the success message
        $('#successModal').modal('show');
        
        // Refresh the page when the modal is closed
        $('#successModal').on('hidden.bs.modal', function (e) {
            location.reload();
        });
    });
});

$('#showAllBtn').click(function() {
    var $btn = $(this);
    var isShowingHidden = $btn.data('showing-hidden');

    if (!isShowingHidden) {
        // Show all rows
        $('#table tr').show();

        // Apply a red background to originally hidden rows
        $('tr[data-index]').each(function() {
            var $row = $(this);
            if ($row.find('input[name="btSelectItem"]').prop('checked')) {
                $row.find('td').css('background-color', 'lightgray'); // Apply to <td> elements
            }
        });
        
        // Update the button text and state
        $btn.text('Hide selected rows');
        $btn.data('showing-hidden', true);
    } else {
        // Hide the rows that are marked as hidden and reset their background
        $('tr[data-index]').each(function() {
            var $row = $(this);
            if ($row.find('input[name="btSelectItem"]').prop('checked')) {
                $row.hide();
                $row.find('td').css('background-color', ''); // Reset the background
            }
        });

        // Update the button text and state
        $btn.text('Show All');
        $btn.data('showing-hidden', false);
    }
});