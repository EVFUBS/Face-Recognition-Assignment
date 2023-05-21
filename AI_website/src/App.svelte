<script lang="ts">
  import Upload from "./lib/Upload.svelte";

  let mode: boolean = false;
  
  let register: string[] = [];

  const registerIdentity = (name: string) => {
    register = [...register, name];
  }

  const unregisterFace = (name: string) => {
    register = register.filter(n => n !== name);
  }

</script>

<main>
  <header>
    <h3>Face Registration</h3>
    <div class="switch-container">
      <p>Image</p>
      <label class="switch">
        <input type="checkbox" bind:checked={mode}/>
        <span class="slider"></span>
      </label>
      <p>Webcam</p>
    </div>
  </header>
  <div class="main-container">
    <div></div>
    <Upload mode={mode} registerFunc={registerIdentity} />
    <div class="register">
      <h5>Registered:</h5>
      <ul>
        {#each register as name}
          <li on:click={() => unregisterFace(name)}>{name}</li>
        {/each}
      </ul>
    </div>
  </div>
</main>




<style>

  main {
    display: flex;
    flex-direction: column;
    height: 90vh;
    font-size: 1.5em;
    color: white;
  }

  .main-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  p {
    font-size: 1rem;
  }

  .switch-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }


  .switch {
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
  }

  .switch input[type="checkbox"] {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: 0.4s;
    border-radius: 34px;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
  }

  input:checked + .slider {
    background-color: grey;
  }

  input:checked + .slider:before {
    transform: translateX(26px);
  }

  .register {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .register ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .register h5 {
    margin: 0;
  }

  .register li:hover {
    cursor: pointer;
    text-decoration: line-through;
  }

</style>