# flappybirdclone

<button onclick="copyToClipboard('Hello, clipboard!')">Copy to Clipboard</button>

<script>
  function copyToClipboard(text) {
    const el = document.createElement('textarea');
    el.value = text;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    alert('Copied to clipboard: ' + text);
  }
</script>
