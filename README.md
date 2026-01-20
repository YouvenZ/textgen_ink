Collecting workspace information# AI Text Generator for Inkscape

[![Inkscape](https://img.shields.io/badge/Inkscape-1.0+-blue.svg)](https://inkscape.org/)
[![Python](https://img.shields.io/badge/Python-3.6+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Generate and transform text in Inkscape using local AI models (Ollama, llamafile)**

A powerful Inkscape extension that leverages local Large Language Models to create, modify, translate, summarize, expand, and rewrite text directly within your designs. Privacy-focused with no cloud dependencies.

---

## 📋 Table of Contents

- Features
- Requirements
- Installation
- Quick Start
- Usage Guide
- Configuration
- Examples
- Troubleshooting
- Contributing
- License

---

## ✨ Features

- **🤖 Multiple AI Providers**
  - **Ollama**: Popular local LLM runner
  - **llamafile**: Single-file executable LLMs
  - **Custom API**: Any OpenAI-compatible endpoint

- **📝 Six Operation Modes**
  | Mode | Description |
  |------|-------------|
  | **Create** | Generate new text from a prompt |
  | **Modify** | Change selected text based on instructions |
  | **Translate** | Convert text to another language |
  | **Summarize** | Condense text to key points |
  | **Expand** | Add detail and elaboration |
  | **Rewrite** | Improve grammar, clarity, and style |

- **🎨 Rich Styling Options**
  - Font family, size, weight, and style
  - Text color and decorations
  - Background boxes with customizable padding
  - Text alignment and spacing controls
  - Scale multiplier for easy resizing

- **🎯 Smart Positioning**
  - 9 preset positions (center, corners, edges)
  - Cursor/selection-based placement
  - Custom X/Y offsets

- **🔧 Advanced Features**
  - Auto-detect available models
  - Temperature and token limit controls
  - 8 tone presets (formal, casual, humorous, etc.)
  - Automatic markdown cleanup
  - Preserve existing text styles

---

## 📦 Requirements

### Core Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| **Inkscape** | 1.0+ | Vector graphics editor |
| **Python** | 3.6+ | Extension runtime (bundled with Inkscape) |

### AI Backend (Choose One)

<details>
<summary><b>🦙 Option 1: Ollama (Recommended)</b></summary>

Ollama is the easiest way to run local LLMs.

**Installation:**

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from: https://ollama.com/download
```

**Pull a model:**

```bash
# Recommended models
ollama pull llama3.2        # Fast, good quality (2GB)
ollama pull mistral         # Excellent for text (4GB)
ollama pull gemma2          # Google's model (5GB)
ollama pull qwen2.5         # Multilingual (4GB)
```

**Start the server:**

```bash
ollama serve
# Server runs at http://localhost:11434
```

</details>

<details>
<summary><b>📦 Option 2: llamafile</b></summary>

llamafile packages models as single executables.

**Installation:**

1. Download a llamafile from [Mozilla's collection](https://github.com/Mozilla-Ocho/llamafile#quickstart)
2. Make it executable and run:

```bash
# Linux/macOS
chmod +x mistral-7b-instruct-v0.2.Q4_0.llamafile
./mistral-7b-instruct-v0.2.Q4_0.llamafile --server

# Windows
# Just double-click the .llamafile or run:
mistral-7b-instruct-v0.2.Q4_0.llamafile.exe --server
```

Server runs at `http://localhost:8080` by default.

</details>

<details>
<summary><b>⚙️ Option 3: Custom API</b></summary>

Any OpenAI-compatible API endpoint works:

- LM Studio
- LocalAI
- Text Generation WebUI (with --api flag)
- vLLM
- Any other OpenAI-compatible server

</details>

---

## 🚀 Installation

### Step 1: Locate Your Inkscape Extensions Directory

**Windows:**
```
C:\Users\[YourUsername]\AppData\Roaming\inkscape\extensions\
```

**macOS:**
```
~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

**Linux:**
```
~/.config/inkscape/extensions/
```

> 💡 **Tip:** In Inkscape, go to **Edit → Preferences → System** to find your extensions directory.

### Step 2: Install the Extension

1. **Create the extension folder:**
   ```bash
   mkdir -p [extensions-directory]/text_gen
   ```

2. **Copy the files:**
   ```bash
   cp text_gen.py [extensions-directory]/text_gen/
   cp text_gen.inx [extensions-directory]/text_gen/
   ```

3. **Set permissions** (Linux/macOS):
   ```bash
   chmod +x [extensions-directory]/text_gen/text_gen.py
   ```

4. **Restart Inkscape**

### Step 3: Verify Installation

Open Inkscape and check: **Extensions → Text → AI Text Generator**

---

## 🎯 Quick Start

### Generate New Text

1. Open Inkscape
2. Go to **Extensions → Text → AI Text Generator**
3. In the **Mode** tab, select **Create**
4. In the **Prompt** tab, enter your prompt:
   ```
   Write a catchy tagline for a coffee shop
   ```
5. Click **Apply**

### Translate Existing Text

1. Select a text object in your document
2. Open **Extensions → Text → AI Text Generator**
3. Select **Translate** mode
4. Choose target language (e.g., "French")
5. Click **Apply**

---

## 📖 Usage Guide

### Tab Overview

| Tab | Purpose |
|-----|---------|
| **Mode** | Select operation (create, modify, translate, etc.) |
| **Prompt** | Enter your text generation prompt |
| **Style** | Configure font, color, and decorations |
| **Layout** | Set alignment, spacing, and positioning |
| **Background** | Add optional background box |
| **API Config** | Configure AI provider and model |
| **Advanced** | Fine-tune generation parameters |

### Operation Modes

#### 🆕 Create Mode
Generate new text from scratch.

```
Prompt: "Write a professional bio for a graphic designer"
```

#### ✏️ Modify Mode
Change selected text based on instructions.

```
Selected text: "Our product is good"
Prompt: "Make it more enthusiastic and professional"
Result: "Our product delivers exceptional results that exceed expectations"
```

#### 🌍 Translate Mode
Convert text to another language while preserving meaning.

```
Selected text: "Welcome to our store"
Target language: Spanish
Result: "Bienvenido a nuestra tienda"
```

#### 📝 Summarize Mode
Condense long text to key points.

#### 📚 Expand Mode
Add detail and elaboration to short text.

#### 🔄 Rewrite Mode
Improve grammar, clarity, and style.

### Style Options

| Option | Description | Default |
|--------|-------------|---------|
| Font Family | Any installed font | Arial |
| Font Size | Size in pixels | 24 |
| Font Weight | normal, bold | normal |
| Font Style | normal, italic | normal |
| Text Color | Hex color code | #000000 |
| Text Decoration | underline, overline, line-through | none |
| Text Scale | Multiplier (0.5 = half, 2.0 = double) | 1.0 |

### Position Modes

```
┌─────────────────────────────────────┐
│ top_left    top_center    top_right │
│                                     │
│ middle_left   center   middle_right │
│                                     │
│ bottom_left bottom_center bottom_right │
└─────────────────────────────────────┘
```

- **cursor**: Place at selected object's center
- **Custom offsets**: Add X/Y offset to any position

### Tone Presets

| Tone | Effect |
|------|--------|
| formal | Professional, business language |
| casual | Conversational, relaxed |
| professional | Corporate, polished |
| friendly | Warm, approachable |
| enthusiastic | Energetic, excited |
| humorous | Witty, playful |
| serious | Straightforward, no-nonsense |
| poetic | Artistic, metaphorical |

---

## ⚙️ Configuration

### API Configuration Tab

| Setting | Description | Default |
|---------|-------------|---------|
| **Provider** | ollama, llamafile, or custom | ollama |
| **API URL** | Server address | http://localhost:11434 |
| **Model** | Model name (leave empty for auto-detect) | (auto) |
| **Auto-detect** | Automatically find available model | ✓ |

### Advanced Tab

| Setting | Description | Default |
|---------|-------------|---------|
| **Temperature** | Creativity (0.0 = focused, 1.0 = creative) | 0.7 |
| **Max Tokens** | Maximum response length | 500 |
| **Remove Asterisks** | Strip markdown bold/italic markers | ✓ |
| **Remove Quotes** | Strip surrounding quotation marks | ✓ |
| **Capitalize First** | Ensure first letter is uppercase | ✗ |
| **Preserve Style** | Keep existing text styling when modifying | ✓ |

### Provider-Specific URLs

| Provider | Default URL | Notes |
|----------|-------------|-------|
| Ollama | http://localhost:11434 | Default Ollama port |
| llamafile | http://localhost:8080 | Default llamafile port |
| LM Studio | http://localhost:1234 | Default LM Studio port |

---

## 💡 Examples

### Example 1: Create a Headline

**Settings:**
- Mode: Create
- Prompt: `Write a bold headline for an eco-friendly product launch`
- Tone: Enthusiastic
- Font Size: 48
- Font Weight: Bold

**Result:**
> 🌱 Revolutionize Your World with Sustainable Innovation!

### Example 2: Translate for Multilingual Poster

**Settings:**
- Mode: Translate
- Target Language: Japanese
- Preserve Style: ✓

**Original:** "Innovation starts here"  
**Result:** "イノベーションはここから始まる"

### Example 3: Professional Bio

**Settings:**
- Mode: Create
- Prompt: `Write a 2-sentence professional bio for a UX designer named Sarah`
- Tone: Professional
- Max Tokens: 100

**Result:**
> Sarah is an award-winning UX designer with over 8 years of experience crafting intuitive digital experiences. Her work spans Fortune 500 companies and innovative startups, where she transforms complex challenges into elegant, user-centered solutions.

### Example 4: Expand a Tagline

**Settings:**
- Mode: Expand
- Tone: Friendly

**Original:** "Fresh coffee daily"  
**Result:** "Every morning, we roast our carefully sourced beans to perfection, ensuring each cup delivers the rich, aromatic experience you deserve. Our commitment to freshness means your coffee is never more than 24 hours from roasting to your cup."

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>Extension not appearing in menu</b></summary>

**Solutions:**
1. Verify files are in the correct location:
   ```bash
   ls [extensions-directory]/text_gen/
   # Should show: text_gen.py, text_gen.inx
   ```
2. Check file permissions (Linux/macOS):
   ```bash
   chmod +x text_gen.py
   ```
3. View Inkscape error log:
   - **Edit → Preferences → System → Open Error Log**
4. Restart Inkscape completely

</details>

<details>
<summary><b>Cannot connect to Ollama</b></summary>

**Error:** `Cannot connect to Ollama at http://localhost:11434`

**Solutions:**
1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
2. Check if a model is installed:
   ```bash
   ollama list
   ```
3. Pull a model if needed:
   ```bash
   ollama pull llama3.2
   ```
4. Verify the URL in API Config tab

</details>

<details>
<summary><b>Model not found</b></summary>

**Error:** `model 'xyz' not found`

**Solutions:**
1. List available models:
   ```bash
   ollama list
   ```
2. Pull the required model:
   ```bash
   ollama pull [model-name]
   ```
3. Enable "Auto-detect model" in API Config
4. Manually enter the exact model name

</details>

<details>
<summary><b>Text not appearing in document</b></summary>

**Solutions:**
1. Check the position mode settings
2. Zoom out to see if text is off-canvas
3. Try "center" position mode
4. Check that the AI generated a response (look for errors)

</details>

<details>
<summary><b>Slow response times</b></summary>

**Solutions:**
1. Use a smaller model:
   ```bash
   ollama pull phi3      # 1.5GB, very fast
   ollama pull tinyllama # 600MB, fastest
   ```
2. Reduce max tokens (150-300 for simple tasks)
3. Ensure your system has enough RAM
4. Close other resource-intensive applications

</details>

<details>
<summary><b>Selected text not detected</b></summary>

**Solutions:**
1. Ensure you've selected a **text object** (not a group or path)
2. Click directly on the text with the Selection tool
3. For grouped text, enter the group first (double-click)
4. Check that the text element has actual text content

</details>

### Debug Mode

Enable debug output to diagnose issues:

1. Run Inkscape from terminal:
   ```bash
   inkscape
   ```
2. Debug messages will appear in the terminal
3. Check the Inkscape error log: **Edit → Preferences → System → Open Error Log**

---

## 📊 Model Recommendations

| Use Case | Recommended Model | Size | Speed |
|----------|-------------------|------|-------|
| Quick drafts | `phi3` or `tinyllama` | 1-2GB | ⚡⚡⚡ |
| General text | `llama3.2` or `mistral` | 4GB | ⚡⚡ |
| Translation | `qwen2.5` | 4GB | ⚡⚡ |
| Creative writing | `llama3.1:8b` | 8GB | ⚡ |
| Best quality | `llama3.1:70b` | 40GB | 🐢 |

---

## 📁 File Structure

```
text_gen/
├── text_gen.py          # Main extension code
├── text_gen.inx         # Inkscape extension definition
└── README.md            # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Setup:**
```bash
git clone https://github.com/YouvenZ/textgen_ink.git
cd textgen_ink
# Symlink to extensions directory for testing
ln -s $(pwd) ~/.config/inkscape/extensions/text_gen
```

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/YouvenZ/textgen_ink/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YouvenZ/textgen_ink/discussions)
- **Email**: youvenz.pro@gmail.com

---

## 🙏 Acknowledgments

- Built on [Inkscape Extension API](https://inkscape.gitlab.io/extensions/documentation/)
- Powered by [Ollama](https://ollama.com/) and [llamafile](https://github.com/Mozilla-Ocho/llamafile)
- Inspired by the need for local, privacy-respecting AI tools

---

## 🔄 Changelog

### v1.0.0 (2024)
- ✨ Initial release
- ✅ Ollama integration
- ✅ llamafile support
- ✅ 6 operation modes
- ✅ Auto model detection
- ✅ Rich styling options
- ✅ 8 tone presets
- ✅ Background box support
- ✅ Markdown cleanup