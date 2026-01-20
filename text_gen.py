#!/usr/bin/env python3
"""
Inkscape extension to generate and modify text using local LLM (Ollama, llamafile).
"""

import inkex
from inkex import TextElement, Rectangle, Group, Tspan, FlowRoot, FlowPara
import re
import urllib.request
import json
import ssl


class AITextGenerator(inkex.EffectExtension):
    """Extension to generate and modify text using local LLM."""
    
    def add_arguments(self, pars):
        pars.add_argument("--tab", type=str, default="mode", help="Active tab")
        pars.add_argument("--operation_mode", type=str, default="create", help="Operation mode")
        
        # API Configuration
        pars.add_argument("--api_provider", type=str, default="ollama", help="API provider")
        pars.add_argument("--api_url", type=str, default="http://localhost:11434", help="Local API URL")
        pars.add_argument("--prompt", type=str, default="", help="User prompt")
        pars.add_argument("--local_model", type=str, default="", help="Local model name")
        pars.add_argument("--target_language", type=str, default="French", help="Target language for translation")
        
        # Style parameters
        pars.add_argument("--font_family", type=str, default="Arial", help="Font family")
        pars.add_argument("--font_size", type=int, default=24, help="Font size")
        pars.add_argument("--font_weight", type=str, default="normal", help="Font weight")
        pars.add_argument("--font_style", type=str, default="normal", help="Font style")
        pars.add_argument("--text_decoration", type=str, default="none", help="Text decoration")
        pars.add_argument("--text_scale", type=float, default=1.0, help="Text scale multiplier")
        
        # Color parameters
        pars.add_argument("--text_color", type=str, default="#000000", help="Text color")
        pars.add_argument("--use_background", type=inkex.Boolean, default=False, help="Use background")
        pars.add_argument("--bg_color", type=str, default="#FFFFFF", help="Background color")
        pars.add_argument("--bg_opacity", type=float, default=0.8, help="Background opacity")
        pars.add_argument("--bg_padding", type=int, default=10, help="Background padding")
        
        # Layout parameters
        pars.add_argument("--text_align", type=str, default="start", help="Text alignment")
        pars.add_argument("--line_height", type=float, default=1.2, help="Line height")
        pars.add_argument("--letter_spacing", type=float, default=0.0, help="Letter spacing")
        pars.add_argument("--word_spacing", type=float, default=0.0, help="Word spacing")
        pars.add_argument("--max_width", type=int, default=600, help="Max text width")
        pars.add_argument("--position_mode", type=str, default="center", help="Position mode")
        pars.add_argument("--x_offset", type=float, default=0.0, help="X position offset")
        pars.add_argument("--y_offset", type=float, default=0.0, help="Y position offset")
        
        # Advanced parameters
        pars.add_argument("--temperature", type=float, default=0.7, help="Temperature")
        pars.add_argument("--max_tokens", type=int, default=500, help="Max tokens")
        pars.add_argument("--tone", type=str, default="none", help="Tone/style")
        pars.add_argument("--preserve_style", type=inkex.Boolean, default=True, help="Preserve style")
        
        # New features
        pars.add_argument("--auto_detect_model", type=inkex.Boolean, default=True, help="Auto-detect model")
        pars.add_argument("--stream_response", type=inkex.Boolean, default=False, help="Stream response")
        pars.add_argument("--remove_asterisks", type=inkex.Boolean, default=True, help="Remove markdown asterisks")
        pars.add_argument("--remove_quotes", type=inkex.Boolean, default=True, help="Remove surrounding quotes")
        pars.add_argument("--capitalize_first", type=inkex.Boolean, default=False, help="Capitalize first letter")
    
    def effect(self):
        """Main effect function."""
        # Validate API configuration
        if not self.options.api_url:
            inkex.errormsg("Please provide a valid API URL for local LLM in the API Config tab.")
            return
        
        # Trim whitespace from inputs
        self.options.api_url = self.options.api_url.strip()
        if self.options.local_model:
            self.options.local_model = self.options.local_model.strip()
        
        # Auto-detect model if enabled and no model specified
        if self.options.auto_detect_model and not self.options.local_model:
            detected_model = self.detect_local_model()
            if detected_model:
                self.options.local_model = detected_model
                inkex.utils.debug(f"Auto-detected model: {detected_model}")
            else:
                inkex.errormsg("Could not auto-detect model. Please specify a model name in the API Config tab.")
                return
        elif not self.options.local_model:
            inkex.errormsg("Please specify a local model name in the API Config tab.")
            return
        
        # Handle different operation modes
        if self.options.operation_mode in ['modify', 'translate', 'summarize', 'expand', 'rewrite']:
            # These modes require selected text
            selected_text = self.get_selected_text()
            if not selected_text:
                inkex.errormsg(f"Please select a text object for {self.options.operation_mode} mode.\nMake sure you've selected a text element (not a group or other object).")
                return
            
            # Generate modified text
            generated_text = self.generate_text_with_context(selected_text['text'])
            
            if generated_text:
                # Modify existing text
                self.modify_text_element(selected_text['element'], generated_text)
        else:
            # Create mode - generate new text
            if not self.options.prompt or len(self.options.prompt.strip()) < 3:
                inkex.errormsg("Please provide a prompt for text generation in the Prompt tab.")
                return
            
            generated_text = self.generate_text()
            
            if generated_text:
                # Create new text element
                self.create_text_element(generated_text)
    
    def detect_local_model(self):
        """Auto-detect available model from local provider."""
        try:
            base_url = self.options.api_url.rstrip('/')
            context = ssl._create_unverified_context()
            
            if self.options.api_provider == "ollama":
                # Try Ollama tags endpoint
                url = f"{base_url}/api/tags"
                req = urllib.request.Request(url, method='GET')
                
                with urllib.request.urlopen(req, timeout=5, context=context) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if 'models' in result and len(result['models']) > 0:
                        # Return the first available model name
                        model_name = result['models'][0].get('name', '')
                        return model_name
            
            elif self.options.api_provider == "llamafile":
                # Try llamafile models endpoint
                url = f"{base_url}/v1/models"
                req = urllib.request.Request(url, method='GET')
                
                with urllib.request.urlopen(req, timeout=5, context=context) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    if 'data' in result and len(result['data']) > 0:
                        # Return the first available model
                        return result['data'][0].get('id', 'LLaMA_CPP')
        
        except Exception as e:
            inkex.utils.debug(f"Could not auto-detect model: {str(e)}")
        
        return None
    
    def get_selected_text(self):
        """Get text from selected text element."""
        # Check if there's any selection
        if not self.svg.selection:
            return None
        
        # Iterate through selection
        for elem in self.svg.selection:
            # Direct text element
            if isinstance(elem, TextElement):
                text_content = self.extract_text_from_element(elem)
                if text_content:
                    return {
                        'element': elem,
                        'text': text_content,
                        'style': elem.style
                    }
            
            # Flow text element
            elif isinstance(elem, FlowRoot):
                text_content = self.extract_text_from_flowroot(elem)
                if text_content:
                    return {
                        'element': elem,
                        'text': text_content,
                        'style': elem.style
                    }
            
            # Check if it's a group containing text
            elif isinstance(elem, Group):
                text_elem = self.find_text_in_group(elem)
                if text_elem:
                    text_content = self.extract_text_from_element(text_elem)
                    if text_content:
                        return {
                            'element': text_elem,
                            'text': text_content,
                            'style': text_elem.style
                        }
            
            # Try to find text elements in children
            else:
                for child in elem.iter():
                    if isinstance(child, TextElement):
                        text_content = self.extract_text_from_element(child)
                        if text_content:
                            return {
                                'element': child,
                                'text': text_content,
                                'style': child.style
                            }
        
        return None
    
    def find_text_in_group(self, group):
        """Find first text element in a group."""
        for child in group:
            if isinstance(child, TextElement):
                return child
            elif isinstance(child, FlowRoot):
                return child
            elif isinstance(child, Group):
                result = self.find_text_in_group(child)
                if result:
                    return result
        return None
    
    def extract_text_from_flowroot(self, elem):
        """Extract text from FlowRoot element."""
        text_parts = []
        for child in elem.iter():
            if isinstance(child, FlowPara):
                if child.text:
                    text_parts.append(child.text)
                for subchild in child:
                    if subchild.text:
                        text_parts.append(subchild.text)
                    if subchild.tail:
                        text_parts.append(subchild.tail)
        return ' '.join(text_parts).strip()
    
    def extract_text_from_element(self, elem):
        """Extract all text content from text element including tspans."""
        text_parts = []
        
        if elem.text:
            text_parts.append(elem.text)
        
        for child in elem:
            if isinstance(child, Tspan):
                if child.text:
                    text_parts.append(child.text)
                if child.tail:
                    text_parts.append(child.tail)
            elif hasattr(child, 'text') and child.text:
                text_parts.append(child.text)
            
            if hasattr(child, 'tail') and child.tail:
                text_parts.append(child.tail)
        
        if hasattr(elem, 'tail') and elem.tail:
            text_parts.append(elem.tail)
        
        return ' '.join(text_parts).strip()
    

    def build_text_style(self):
        """Build text style dictionary."""
        style = {}
        
        # Apply scale to font size
        scaled_font_size = self.options.font_size * self.options.text_scale
        
        style['font-family'] = self.options.font_family
        style['font-size'] = f'{scaled_font_size}px'
        style['font-weight'] = self.options.font_weight
        style['font-style'] = self.options.font_style
        style['fill'] = self.options.text_color
        style['text-anchor'] = self.options.text_align
        
        if self.options.text_decoration and self.options.text_decoration != 'none':
            valid_decorations = ['underline', 'overline', 'line-through']
            if self.options.text_decoration in valid_decorations:
                style['text-decoration'] = self.options.text_decoration
        
        if self.options.letter_spacing != 0:
            style['letter-spacing'] = f'{self.options.letter_spacing}px'
        
        if self.options.word_spacing != 0:
            style['word-spacing'] = f'{self.options.word_spacing}px'
        
        return style



    def generate_text(self):
        """Generate new text based on prompt."""
        prompt = self.build_create_prompt()
        return self.call_llm_api(prompt)
    
    def generate_text_with_context(self, existing_text):
        """Generate text based on existing text and operation mode."""
        prompt = self.build_context_prompt(existing_text)
        return self.call_llm_api(prompt)
    
    def build_create_prompt(self):
        """Build prompt for creating new text."""
        prompt_parts = [self.options.prompt]
        
        # Add tone instruction
        if self.options.tone != "none":
            tone_instructions = {
                'formal': 'Use formal language and professional tone.',
                'casual': 'Use casual, conversational language.',
                'professional': 'Use professional business language.',
                'friendly': 'Use friendly and warm tone.',
                'enthusiastic': 'Use enthusiastic and energetic language.',
                'humorous': 'Add humor and wit.',
                'serious': 'Use serious and straightforward tone.',
                'poetic': 'Use poetic and artistic language.'
            }
            prompt_parts.append(tone_instructions.get(self.options.tone, ''))
        
        prompt_parts.append("\nIMPORTANT: Return ONLY the text content, no explanations or formatting markers.")
        
        return '\n'.join(prompt_parts)
    
    def build_context_prompt(self, existing_text):
        """Build prompt for modifying existing text."""
        mode_instructions = {
            'modify': f"Modify the following text based on this instruction: {self.options.prompt}\n\nOriginal text: {existing_text}",
            'translate': f"Translate the following text to {self.options.target_language}. Maintain the meaning and tone.\n\nOriginal text: {existing_text}",
            'summarize': f"Summarize the following text to be shorter and more concise while keeping key points.\n\nOriginal text: {existing_text}",
            'expand': f"Expand and elaborate on the following text with more detail and examples.\n\nOriginal text: {existing_text}",
            'rewrite': f"Rewrite and improve the following text for better grammar, clarity, and style.\n\nOriginal text: {existing_text}"
        }
        
        prompt = mode_instructions.get(self.options.operation_mode, existing_text)
        
        # Add tone instruction
        if self.options.tone != "none":
            tone_instructions = {
                'formal': '\nUse formal language.',
                'casual': '\nUse casual language.',
                'professional': '\nUse professional tone.',
                'friendly': '\nUse friendly tone.',
                'enthusiastic': '\nUse enthusiastic tone.',
                'humorous': '\nAdd humor.',
                'serious': '\nUse serious tone.',
                'poetic': '\nUse poetic language.'
            }
            prompt += tone_instructions.get(self.options.tone, '')
        
        prompt += "\n\nIMPORTANT: Return ONLY the text content, no explanations or formatting markers."
        
        return prompt
    
    def call_llm_api(self, prompt):
        """Call LLM API to generate text (supports Ollama, llamafile, and other local providers)."""
        
        if self.options.api_provider == "ollama":
            return self.call_ollama_api(prompt)
        elif self.options.api_provider == "llamafile":
            return self.call_llamafile_api(prompt)
        elif self.options.api_provider == "custom":
            return self.call_custom_api(prompt)
        else:
            inkex.errormsg(f"Unknown API provider: {self.options.api_provider}")
            return None
    
    def call_ollama_api(self, prompt):
        """Call Ollama API."""
        base_url = self.options.api_url.rstrip('/')
        url = f"{base_url}/api/generate"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Build system prompt
        system_prompt = "You are a helpful text generator. You respond with only the requested text content, without any explanations, formatting markers, or additional commentary."
        full_prompt = f"{system_prompt}\n\nUser request: {prompt}"
        
        # Ollama API format
        data = {
            'model': self.options.local_model,
            'prompt': full_prompt,
            'stream': False,  # Disable streaming for reliability
            'options': {
                'temperature': self.options.temperature,
                'num_predict': self.options.max_tokens
            }
        }
        
        # Convert to JSON bytes
        json_data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            url,
            data=json_data,
            headers=headers,
            method='POST'
        )
        
        # Debug output
        inkex.utils.debug(f"=== Ollama Request ===")
        inkex.utils.debug(f"URL: {url}")
        inkex.utils.debug(f"Model: {self.options.local_model}")
        inkex.utils.debug(f"Temperature: {self.options.temperature}")
        inkex.utils.debug(f"Max tokens: {self.options.max_tokens}")
        
        context = ssl._create_unverified_context()
        
        try:
            with urllib.request.urlopen(req, timeout=120, context=context) as response:
                response_data = response.read().decode('utf-8')
                inkex.utils.debug(f"Response (first 300 chars): {response_data[:300]}")
                
                result = json.loads(response_data)
                
                if 'response' in result:
                    text = result['response'].strip()
                    text = self.clean_text_response(text)
                    inkex.utils.debug(f"Cleaned text (first 200 chars): {text[:200]}")
                    return text
                else:
                    inkex.errormsg(f"Unexpected Ollama response format. Keys: {list(result.keys())}")
                    return None
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            inkex.errormsg(f"Ollama HTTP Error {e.code}:\n{error_body}\n\nURL: {url}\nModel: {self.options.local_model}\n\nMake sure:\n1. Ollama is running: ollama serve\n2. Model is pulled: ollama pull {self.options.local_model}")
            return None
        
        except urllib.error.URLError as e:
            inkex.errormsg(f"Cannot connect to Ollama at {url}\n\nError: {str(e)}\n\nMake sure:\n1. Ollama is running: ollama serve\n2. URL is correct: {self.options.api_url}\n3. Model is pulled: ollama pull {self.options.local_model}")
            return None
        
        except json.JSONDecodeError as e:
            inkex.errormsg(f"Invalid JSON response from Ollama:\n{str(e)}\n\nThis usually means Ollama returned an error message instead of JSON.")
            return None
        
        except Exception as e:
            inkex.errormsg(f"Unexpected error calling Ollama:\n{type(e).__name__}: {str(e)}")
            import traceback
            inkex.utils.debug(traceback.format_exc())
            return None
    
    def _handle_ollama_stream(self, req, context):
        """Handle streaming response from Ollama."""
        full_response = ""
        try:
            with urllib.request.urlopen(req, timeout=120, context=context) as response:
                for line in response:
                    if line:
                        line_str = line.decode('utf-8').strip()
                        if line_str:
                            try:
                                chunk = json.loads(line_str)
                                if 'response' in chunk:
                                    full_response += chunk['response']
                            except json.JSONDecodeError:
                                continue
            
            return self.clean_text_response(full_response.strip()) if full_response else None
        except Exception as e:
            inkex.errormsg(f"Error streaming from Ollama: {str(e)}")
            return None
    
    def call_llamafile_api(self, prompt):
        """Call llamafile API."""
        base_url = self.options.api_url.rstrip('/')
        url = f"{base_url}/v1/chat/completions"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # llamafile uses OpenAI-compatible format
        data = {
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful text generator. You respond with only the requested text content, without any explanations, formatting markers, or additional commentary.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': self.options.temperature,
            'max_tokens': self.options.max_tokens
        }
        
        # Only add model if specified
        if self.options.local_model:
            data['model'] = self.options.local_model
        
        return self._make_api_request(url, headers, data, provider="llamafile", timeout=120)
    
    def call_custom_api(self, prompt):
        """Call custom local API provider (OpenAI-compatible format)."""
        base_url = self.options.api_url.rstrip('/')
        url = f"{base_url}/v1/chat/completions"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Use OpenAI-compatible format for custom providers
        data = {
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a helpful text generator. You respond with only the requested text content, without any explanations, formatting markers, or additional commentary.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'temperature': self.options.temperature,
            'max_tokens': self.options.max_tokens
        }
        
        # Only add model if specified
        if self.options.local_model:
            data['model'] = self.options.local_model
        
        return self._make_api_request(url, headers, data, provider="Custom API", timeout=120)
    
    def _make_api_request(self, url, headers, data, provider="API", timeout=60):
        """Make HTTP request to API."""
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        context = ssl._create_unverified_context()
        
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=context) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if 'choices' in result and len(result['choices']) > 0:
                    text = result['choices'][0]['message']['content'].strip()
                    text = self.clean_text_response(text)
                    return text
                else:
                    raise Exception(f"No choices in {provider} API response")
        
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            try:
                error_data = json.loads(error_body)
                error_message = error_data.get('error', {}).get('message', str(e))
            except:
                error_message = error_body
            
            if provider == "llamafile":
                inkex.errormsg(f"{provider} API Error: {error_message}\n\nMake sure llamafile is running at {self.options.api_url}")
            else:
                inkex.errormsg(f"{provider} API Error: {error_message}")
            return None
        
        except urllib.error.URLError as e:
            if provider == "llamafile":
                inkex.errormsg(f"Cannot connect to llamafile at {url}\n\nMake sure:\n1. llamafile executable is running\n2. Server is accessible at {self.options.api_url}")
            else:
                inkex.errormsg(f"Cannot connect to {provider}: {str(e)}")
            return None
        
        except Exception as e:
            inkex.errormsg(f"Error calling {provider}: {str(e)}")
            return None
    
    def clean_text_response(self, text):
        """Clean up text response from API."""
        # Remove markdown code blocks
        text = re.sub(r'^```.*?\n', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n```$', '', text, flags=re.MULTILINE)
        text = re.sub(r'```', '', text)
        
        # Remove markdown asterisks if enabled
        if self.options.remove_asterisks:
            text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)  # Bold
            text = re.sub(r'\*([^\*]+)\*', r'\1', text)  # Italic
            text = re.sub(r'__([^_]+)__', r'\1', text)  # Bold
            text = re.sub(r'_([^_]+)_', r'\1', text)  # Italic
        
        # Remove quotes if the entire text is quoted and option is enabled
        if self.options.remove_quotes:
            if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
                text = text[1:-1]
        
        # Capitalize first letter if enabled
        if self.options.capitalize_first and text:
            text = text[0].upper() + text[1:] if len(text) > 1 else text.upper()
        
        return text.strip()
    
    def create_text_element(self, text):
        """Create new text element with generated text."""
        # Calculate position
        position = self.calculate_position()
        
        # Create group for text and optional background
        group = Group()
        group.set('id', self.svg.get_unique_id('ai-text'))
        
        # Wrap text if needed
        wrapped_lines = self.wrap_text(text)
        
        # Create text element
        text_elem = TextElement()
        text_elem.set('x', str(position['x']))
        text_elem.set('y', str(position['y']))
        
        # Set text style (includes scaling)
        style_dict = self.build_text_style()
        text_elem.style = style_dict
        
        # Add text lines with scaled line height
        scaled_font_size = self.options.font_size * self.options.text_scale
        line_height_px = scaled_font_size * self.options.line_height
        
        for i, line in enumerate(wrapped_lines):
            if i == 0:
                text_elem.text = line
            else:
                tspan = Tspan()
                tspan.text = line
                tspan.set('x', str(position['x']))
                tspan.set('dy', str(line_height_px))
                text_elem.append(tspan)
        
        # Add background if requested
        if self.options.use_background:
            bbox = self.estimate_text_bbox(wrapped_lines, position)
            bg_rect = self.create_background_rect(bbox)
            group.append(bg_rect)
        
        group.append(text_elem)
        
        # Add to current layer
        self.svg.get_current_layer().append(group)


    def modify_text_element(self, text_elem, new_text):
        """Modify existing text element with new text."""
        # Handle FlowRoot differently
        if isinstance(text_elem, FlowRoot):
            self.modify_flowroot_element(text_elem, new_text)
            return
        
        # Wrap new text
        wrapped_lines = self.wrap_text(new_text)
        
        # Get current position
        x = text_elem.get('x', '0')
        y = text_elem.get('y', '0')
        
        # Clear existing content
        text_elem.text = ''
        for child in list(text_elem):
            text_elem.remove(child)
        
        # Determine if we should preserve style
        if self.options.preserve_style:
            # Keep existing style
            existing_font_size = text_elem.style.get('font-size', f'{self.options.font_size}px')
            try:
                font_size = float(existing_font_size.replace('px', '').replace('pt', ''))
            except:
                font_size = self.options.font_size
            # Apply scale to existing font size
            scaled_font_size = font_size * self.options.text_scale
            text_elem.style['font-size'] = f'{scaled_font_size}px'
            line_height_px = scaled_font_size * self.options.line_height
        else:
            # Apply new style (includes scaling)
            style_dict = self.build_text_style()
            text_elem.style = style_dict
            scaled_font_size = self.options.font_size * self.options.text_scale
            line_height_px = scaled_font_size * self.options.line_height
        
        # Add new text lines
        for i, line in enumerate(wrapped_lines):
            if i == 0:
                text_elem.text = line
            else:
                tspan = Tspan()
                tspan.text = line
                tspan.set('x', x)
                tspan.set('dy', str(line_height_px))
                text_elem.append(tspan)
                
                    
    def modify_flowroot_element(self, flowroot, new_text):
        """Modify FlowRoot element with new text."""
        # Find FlowPara element
        flow_para = None
        for child in flowroot:
            if isinstance(child, FlowPara):
                flow_para = child
                break
        
        if flow_para is not None:
            # Clear existing content
            flow_para.text = new_text
            for child in list(flow_para):
                flow_para.remove(child)
        else:
            # Create new FlowPara if none exists
            flow_para = FlowPara()
            flow_para.text = new_text
            flowroot.append(flow_para)
    
    def build_text_style(self):
        """Build text style dictionary."""
        style = {}
        
        style['font-family'] = self.options.font_family
        style['font-size'] = f'{self.options.font_size}px'
        style['font-weight'] = self.options.font_weight
        style['font-style'] = self.options.font_style
        style['fill'] = self.options.text_color
        style['text-anchor'] = self.options.text_align
        
        if self.options.text_decoration and self.options.text_decoration != 'none':
            valid_decorations = ['underline', 'overline', 'line-through']
            if self.options.text_decoration in valid_decorations:
                style['text-decoration'] = self.options.text_decoration
        
        if self.options.letter_spacing != 0:
            style['letter-spacing'] = f'{self.options.letter_spacing}px'
        
        if self.options.word_spacing != 0:
            style['word-spacing'] = f'{self.options.word_spacing}px'
        
        return style
    
    def wrap_text(self, text):
        """Wrap text to max width."""
        # Apply scale to calculations
        scaled_font_size = self.options.font_size * self.options.text_scale
        char_width = scaled_font_size * 0.6
        max_chars = int(self.options.max_width / char_width)
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            if current_length + word_length + len(current_line) <= max_chars:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines if lines else [text]
    
    def calculate_position(self):
        """Calculate position based on position mode."""
        # Get document dimensions
        try:
            doc_width = float(self.svg.get('width').replace('px', '').replace('mm', '').replace('pt', ''))
        except:
            doc_width = self.svg.viewport_width or 800
        
        try:
            doc_height = float(self.svg.get('height').replace('px', '').replace('mm', '').replace('pt', ''))
        except:
            doc_height = self.svg.viewport_height or 600
        
        # Define base positions
        positions = {
            'center': {'x': doc_width / 2, 'y': doc_height / 2},
            'top_left': {'x': 50, 'y': 50},
            'top_center': {'x': doc_width / 2, 'y': 50},
            'top_right': {'x': doc_width - 50, 'y': 50},
            'bottom_left': {'x': 50, 'y': doc_height - 50},
            'bottom_center': {'x': doc_width / 2, 'y': doc_height - 50},
            'bottom_right': {'x': doc_width - 50, 'y': doc_height - 50},
            'middle_left': {'x': 50, 'y': doc_height / 2},
            'middle_right': {'x': doc_width - 50, 'y': doc_height / 2}
        }
        
        # Handle cursor/selection position
        if self.options.position_mode == 'cursor':
            if self.svg.selection:
                for elem in self.svg.selection:
                    bbox = elem.bounding_box()
                    if bbox:
                        return {
                            'x': bbox.center_x + self.options.x_offset,
                            'y': bbox.center_y + self.options.y_offset
                        }
            # Fallback to center if no selection
            return {
                'x': doc_width / 2 + self.options.x_offset,
                'y': doc_height / 2 + self.options.y_offset
            }
        
        # Get base position
        base_pos = positions.get(self.options.position_mode, positions['center'])
        
        # Apply offsets
        return {
            'x': base_pos['x'] + self.options.x_offset,
            'y': base_pos['y'] + self.options.y_offset
        }    
    def estimate_text_bbox(self, lines, position):
        """Estimate bounding box for text."""
        # Apply scale to calculations
        scaled_font_size = self.options.font_size * self.options.text_scale
        char_width = scaled_font_size * 0.6
        line_height = scaled_font_size * self.options.line_height
        
        max_line_length = max(len(line) for line in lines) if lines else 0
        width = max_line_length * char_width
        height = len(lines) * line_height
        
        # Calculate x position based on alignment
        if self.options.text_align == 'middle':
            x = position['x'] - width / 2
        elif self.options.text_align == 'end':
            x = position['x'] - width
        else:  # start
            x = position['x']
        
        # Y position starts at the top of the first line
        y = position['y'] - scaled_font_size
        
        return {
            'x': x - self.options.bg_padding,
            'y': y - self.options.bg_padding,
            'width': width + self.options.bg_padding * 2,
            'height': height + self.options.bg_padding * 2
        }    
    def create_background_rect(self, bbox):
        """Create background rectangle."""
        rect = Rectangle()
        rect.set('x', str(bbox['x']))
        rect.set('y', str(bbox['y']))
        rect.set('width', str(bbox['width']))
        rect.set('height', str(bbox['height']))
        
        rect.style = {
            'fill': self.options.bg_color,
            'fill-opacity': str(self.options.bg_opacity),
            'stroke': 'none'
        }
        
        return rect


if __name__ == '__main__':
    AITextGenerator().run()