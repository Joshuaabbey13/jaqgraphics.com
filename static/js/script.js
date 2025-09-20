document.getElementById('edit-button').addEventListener('click', () => {
    const imageInput = document.getElementById('image-input');
    const promptInput = document.getElementById('prompt-input');
    const resultImage = document.getElementById('result-image');

    if (imageInput.files.length === 0) {
        alert('Please select an image first.');
        return;
    }

    const formData = new FormData();
    formData.append('file', imageInput.files[0]);
    formData.append('prompt', promptInput.value);

    fetch('/edit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = URL.createObjectURL(blob);
        resultImage.src = url;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while editing the image.');
    });
});
