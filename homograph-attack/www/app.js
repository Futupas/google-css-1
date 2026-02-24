'use strict';

let font;

// Load the font file. Using a WOFF2 file for efficiency.
opentype.load('/arial.ttf', function(err, loadedFont) {
    if (err) {
        document.getElementById('loader').textContent = 'Chyba při načítání písma: ' + err;
        return;
    }
    font = loadedFont;
    document.getElementById('loader').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
    analyze();
});

function levenshteinDistance(a, b) {
    if (a.length === 0) return b.length;
    if (b.length === 0) return a.length;
    const matrix = Array(b.length + 1).fill(null).map(() => Array(a.length + 1).fill(null));
    for (let i = 0; i <= a.length; i += 1) matrix[0][i] = i;
    for (let j = 0; j <= b.length; j += 1) matrix[j][0] = j;
    for (let j = 1; j <= b.length; j += 1) {
        for (let i = 1; i <= a.length; i += 1) {
            const indicator = a[i - 1] === b[j - 1] ? 0 : 1;
            matrix[j][i] = Math.min(
                matrix[j][i - 1] + 1, // deletion
                matrix[j - 1][i] + 1, // insertion
                matrix[j - 1][i - 1] + indicator, // substitution
            );
        }
    }
    return matrix[b.length][a.length];
}

function analyze() {
    if (!font) return;

    const text1 = document.getElementById('text1').value;
    const text2 = document.getElementById('text2').value;

    // Get all DOM elements
    const charCodes1Div = document.getElementById('char-codes1');
    const charCodes2Div = document.getElementById('char-codes2');
    const messageDiv = document.getElementById('message');
    const gridVisualDiv = document.getElementById('similarity-grid-visual');
    const overallVisualDiv = document.getElementById('overall-similarity-visual');
    const gridCodeDiv = document.getElementById('similarity-grid-code');
    const overallCodeDiv = document.getElementById('overall-similarity-code');

    // Display raw character codes
    charCodes1Div.textContent = Array.from(text1).map(c => c.charCodeAt(0)).join(' ');
    charCodes2Div.textContent = Array.from(text2).map(c => c.charCodeAt(0)).join(' ');

    // Clear previous results
    messageDiv.textContent = '';
    gridVisualDiv.innerHTML = '';
    overallVisualDiv.innerHTML = '';
    gridCodeDiv.innerHTML = '';
    overallCodeDiv.innerHTML = '';
    console.clear();

    if (text1.length !== text2.length) {
        messageDiv.textContent = "Texty mají různou délku, nelze provést analýzu po jednotlivých znacích.";
        document.getElementById('analysis-results-visual').style.display = 'none';
        document.getElementById('analysis-results-code').style.display = 'none';
        return;
    }

    document.getElementById('analysis-results-visual').style.display = 'block';
    document.getElementById('analysis-results-code').style.display = 'block';

    let totalVisualSimilarity = 0;
    let identicalChars = 0;
    const charArray1 = Array.from(text1);
    const charArray2 = Array.from(text2);

    for (let i = 0; i < charArray1.length; i++) {
        const char1 = charArray1[i];
        const char2 = charArray2[i];

        // --- 1. Visual Similarity Analysis ---
        const glyph1 = font.charToGlyph(char1);
        const glyph2 = font.charToGlyph(char2);
        const path1 = glyph1.getPath(0, 0, 72).toPathData();
        const path2 = glyph2.getPath(0, 0, 72).toPathData();
        
        console.log(`Character Pair ${i+1}: '${char1}' vs '${char2}'`);
        console.log(`'${char1}' SVG Path:`, path1);
        console.log(`'${char2}' SVG Path:`, path2);
        
        const distance = levenshteinDistance(path1, path2);
        const maxLength = Math.max(path1.length, path2.length);
        const visualSimilarity = maxLength > 0 ? (1 - distance / maxLength) * 100 : 100;
        totalVisualSimilarity += visualSimilarity;

        const visualComparisonDiv = document.createElement('div');
        visualComparisonDiv.classList.add('char-comparison');
        visualComparisonDiv.innerHTML = `
            <div class="chars"><b>${char1}</b><span> vs </span><b>${char2}</b></div>
            <div class="similarity-percent">${visualSimilarity.toFixed(2)}% shoda</div>`;
        
        if (visualSimilarity === 100) visualComparisonDiv.classList.add('perfect-match');
        else if (visualSimilarity > 85) visualComparisonDiv.classList.add('high-similarity');
        else visualComparisonDiv.classList.add('no-match');
        gridVisualDiv.appendChild(visualComparisonDiv);

        // --- 2. Code Similarity Analysis ---
        const code1 = char1.charCodeAt(0);
        const code2 = char2.charCodeAt(0);
        const codeComparisonDiv = document.createElement('div');
        codeComparisonDiv.classList.add('char-comparison');
        let codeSimilarity = 0;

        if (code1 === code2) {
            codeSimilarity = 100;
            identicalChars++;
            codeComparisonDiv.classList.add('perfect-match');
        } else {
            codeComparisonDiv.classList.add('no-match');
        }
        
        codeComparisonDiv.innerHTML = `
            <div class="chars"><b>${char1}</b><span> vs </span><b>${char2}</b></div>
            <div class="similarity-percent">${codeSimilarity}% shoda</div>`;
        gridCodeDiv.appendChild(codeComparisonDiv);
    }
    
    // Display overall results
    const avgVisualSimilarity = text1.length > 0 ? totalVisualSimilarity / text1.length : 0;
    overallVisualDiv.innerHTML = `<strong>Průměrná vizuální podobnost: ${avgVisualSimilarity.toFixed(2)}%</strong>`;
    
    const avgCodeSimilarity = text1.length > 0 ? (identicalChars / text1.length) * 100 : 0;
    overallCodeDiv.innerHTML = `<strong>Průměrná shoda kódů: ${avgCodeSimilarity.toFixed(2)}%</strong>`;
}

document.getElementById('text1').addEventListener('input', analyze);
document.getElementById('text2').addEventListener('input', analyze);
