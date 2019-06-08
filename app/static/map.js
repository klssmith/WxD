var lat = document.getElementById("lat").innerText;
var long = document.getElementById("long").innerText;

var map = L.map('mapid').setView([lat, long], 13);
var overviewMap = L.map('overview-map-id').setView([lat, long], 6);

var esriStreets = L.esri.basemapLayer('Streets').addTo(map);
L.marker([lat, long]).addTo(map);

var esriTopographic = L.esri.basemapLayer('Topographic').addTo(overviewMap);
L.marker([lat, long]).addTo(overviewMap);
overviewMap.removeControl(overviewMap.zoomControl);
