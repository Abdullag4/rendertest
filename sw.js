self.addEventListener('install', event => {
  console.log('Service Worker installing…');
});

self.addEventListener('fetch', event => {
  // Simple network‑first strategy:
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
