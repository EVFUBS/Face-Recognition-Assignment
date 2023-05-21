<script lang="ts">
    import { onDestroy, onMount } from "svelte";


    /* modes */
    export let mode:boolean;
    export let registerFunc: (name: string) => void;
    let cameraInUse = false;

    /* image upload and preview */
    let imageInput: HTMLInputElement;
    let preview: HTMLImageElement;

    /* webcam */
    let videoRef: HTMLVideoElement;
    let predictionImage;
    let prediction: string;

    /* webcam functions */
    function startWebcam() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                videoRef.srcObject = stream;
                videoRef.play();
                cameraInUse = true;
            })
            .catch(err => {
                console.error(err);
            });
    }

    function stopWebcam() {
        const stream = videoRef.srcObject as MediaStream;
        const tracks = stream.getTracks();
        tracks.forEach(track => {
            track.stop();
        });
        videoRef.srcObject = null;
        cameraInUse = false;
    }

    /* image upload functions */
    const uploadImage = () => {
        const file = imageInput.files[0];
        predictionImage = file;
        const reader = new FileReader();
        reader.onloadend = () => {
            preview.src = reader.result as string;
        };
        reader.readAsDataURL(file);
    };

    const capture = async() => {
        const canvas = document.createElement('canvas');
        canvas.width = videoRef.videoWidth;
        canvas.height = videoRef.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoRef, 0, 0, canvas.width, canvas.height);
        const dataURI = canvas.toDataURL('image/jpeg');
        predictionImage = await (await fetch(dataURI)).blob();
        predict(new Event('submit'));
    };

    /* prediction */
    const predict = async (e: Event) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', predictionImage);
        const res = await fetch('http://localhost:8000/face_recognition', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        prediction = data.prediction;

        console.log(prediction);
        registerFunc(prediction);
    };
</script>

<div>

    {#if mode}
        <div class="webcam">
            <video bind:this={videoRef} autoplay></video>
            {#if !cameraInUse}
                <button on:click={startWebcam}>Start Webcam</button>
            {:else}
                <button on:click={stopWebcam}>Stop Webcam</button>
            {/if}
            <button on:click={capture}>Capture and Predict</button>
            <p>Prediction: {prediction}</p>
        </div>
    {:else}
        <form on:submit|preventDefault={predict}>
            <img bind:this={preview} />
            <input type="file" accept="image/*" bind:this={imageInput} on:change={uploadImage} />
            <button type="submit">Predict</button>
        </form>

        <p>Prediction: {prediction}</p>
    {/if}
</div>

<style>

    form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        gap: 20px;
    }

    img {
        width: 500px;
        height: 500px;
        object-fit: cover;
    }

    video {
        width: 500px;
        height: 500px;
        object-fit: cover;
    }

    .webcam {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        gap: 20px;
    }
</style>