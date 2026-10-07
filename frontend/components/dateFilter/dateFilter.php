<?php
// Get today's date and first day of month for default values
$today = date('Y-m-d');
$firstDayOfMonth = date('Y-m-01');
?>

<div class="date-filter-container">
    <label for="start-date">Periode:</label>
    <input type="date" id="start-date" value="<?php echo $firstDayOfMonth; ?>">
    
    <span class="date-filter-separator">t/m</span>
    
    <input type="date" id="end-date" value="<?php echo $today; ?>">
    
    <button class="date-filter-button" onclick="applyDateFilter()">Toepassen</button>
    <button class="date-filter-reset" onclick="resetDateFilter()">Reset</button>
</div>
