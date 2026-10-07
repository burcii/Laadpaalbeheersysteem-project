async function editUser(userID) {
    event.preventDefault();

    const email = document.getElementById("email");
    const password = document.getElementById("password");
    const adress = document.getElementById("adress");
    const zipcode = document.getElementById("zipcode");
    const country = document.getElementById("country");
    const firstName = document.getElementById("firstName");
    const nameParticle = document.getElementById("nameParticle");
    const lastName = document.getElementById("lastName");
    const phonenumber = document.getElementById("phonenumber");
    const bankaccount = document.getElementById("bankaccount");

//    console.log(userID);

    try {
        const param = {
            email : email.value ? email.value : "",
            password : password.value ? password.value : "",
            adress : adress.value ? adress.value : "",
            zipcode : zipcode.value ? zipcode.value : "",
            country : country.value ? country.value : "",
            firstName : firstName.value ? firstName.value : "",
            nameParticle : nameParticle.value ? nameParticle.value : "",
            lastName : lastName.value ? lastName.value : "",
            phonenumber : phonenumber.value ? phonenumber.value : "",
            bankaccount : bankaccount.value ? bankaccount.value : "",
        }
        console.log(param);

        const response = await fetch(`http://localhost:8001/edit_user_info/${userID}`, {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(param)
        })

        const data = await response.json();

        if (data.success) {
            alert('Gebruiker succesvol bijgewerkt!');
        } else {
            alert(data.error || 'Er is iets misgegaan bij het bijwerken van de gebruiker.');
        }
    } catch (error) {
        console.error(error);
    }
}