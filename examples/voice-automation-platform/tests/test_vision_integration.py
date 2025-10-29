"""
Vision Integration Tests for ChatKit Platform
Using GLM-4.5V model through Z.ai API

Tests multimodal capabilities including:
- Image analysis
- UI screenshot interpretation
- Visual debugging
- Component recognition
"""

import os
import sys
import base64
import requests
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Set up environment
os.environ["ANTHROPIC_MODEL"] = "glm-4.5V"
os.environ["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"
os.environ["ANTHROPIC_AUTH_TOKEN"] = "665b963943b647dc9501dff942afb877.A47LrMc7sgGjyfBJ"


class VisionTestClient:
    """Client for testing vision capabilities"""
    
    def __init__(self):
        self.base_url = os.getenv("ANTHROPIC_BASE_URL")
        self.auth_token = os.getenv("ANTHROPIC_AUTH_TOKEN")
        self.model = os.getenv("ANTHROPIC_MODEL")
        
    def encode_image(self, image_path: str = None, image: Image.Image = None) -> str:
        """Encode image to base64"""
        if image:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode('utf-8')
        elif image_path:
            with open(image_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
        raise ValueError("Either image_path or image must be provided")
    
    def analyze_image(self, image_data: str, prompt: str) -> dict:
        """Send image to GLM-4.5V for analysis"""
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/v1/messages",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        return response.json()


def create_test_ui_screenshot() -> Image.Image:
    """Create a mock UI screenshot for testing"""
    # Create a 800x600 image with white background
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw header
    draw.rectangle([0, 0, 800, 80], fill='#2563eb')
    draw.text((20, 25), "Voice Automation Platform", fill='white')
    
    # Draw sidebar
    draw.rectangle([0, 80, 200, 600], fill='#f3f4f6')
    draw.text((20, 100), "🎙️ Voice Input", fill='black')
    draw.text((20, 140), "📊 Dashboard", fill='black')
    draw.text((20, 180), "🤖 Agents", fill='black')
    draw.text((20, 220), "🔧 MCP Tools", fill='black')
    
    # Draw main content area
    draw.rectangle([220, 100, 780, 580], fill='white', outline='#e5e7eb')
    draw.text((240, 120), "Active Tasks", fill='black')
    
    # Draw task cards
    for i in range(3):
        y = 160 + (i * 120)
        draw.rectangle([240, y, 760, y+100], fill='#f9fafb', outline='#d1d5db')
        draw.text((260, y+10), f"Task {i+1}: Processing...", fill='black')
        draw.text((260, y+40), f"Status: Active", fill='#10b981')
        draw.rectangle([260, y+70, 360, y+85], fill='#3b82f6')
        draw.text((270, y+72), "View Details", fill='white')
    
    return img


def create_test_error_screenshot() -> Image.Image:
    """Create a mock error UI for testing"""
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw error modal
    draw.rectangle([50, 50, 550, 350], fill='white', outline='#ef4444', width=3)
    draw.text((200, 100), "❌ Error", fill='#dc2626')
    draw.text((100, 150), "Connection to backend failed", fill='#991b1b')
    draw.text((100, 180), "Status Code: 500", fill='#991b1b')
    
    # Draw buttons
    draw.rectangle([150, 250, 250, 290], fill='#ef4444')
    draw.text((170, 262), "Retry", fill='white')
    
    draw.rectangle([300, 250, 400, 290], fill='#9ca3af')
    draw.text((320, 262), "Cancel", fill='white')
    
    return img


def test_ui_component_recognition():
    """Test 1: UI Component Recognition"""
    print("\n" + "="*60)
    print("🎯 TEST 1: UI Component Recognition")
    print("="*60)
    
    client = VisionTestClient()
    ui_image = create_test_ui_screenshot()
    image_data = client.encode_image(image=ui_image)
    
    prompt = """
    Analyze this UI screenshot and identify:
    1. What type of application interface is this?
    2. List all visible UI components (buttons, sidebars, cards, etc.)
    3. Describe the layout structure
    4. What actions can a user take based on visible elements?
    5. Are there any accessibility concerns?
    
    Provide a structured analysis.
    """
    
    print("\n📤 Sending UI screenshot to GLM-4.5V...")
    result = client.analyze_image(image_data, prompt)
    
    if result and 'content' in result:
        analysis = result['content'][0]['text']
        print("\n✅ Vision Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        return True
    else:
        print("❌ Test failed - no response")
        return False


def test_error_detection():
    """Test 2: Error State Detection"""
    print("\n" + "="*60)
    print("🎯 TEST 2: Error State Detection")
    print("="*60)
    
    client = VisionTestClient()
    error_image = create_test_error_screenshot()
    image_data = client.encode_image(image=error_image)
    
    prompt = """
    This screenshot shows an error state in a web application.
    
    Please identify:
    1. What type of error is displayed?
    2. What information is provided to the user?
    3. What actions can the user take?
    4. Is the error message clear and helpful?
    5. Suggest improvements for this error UI
    """
    
    print("\n📤 Sending error screenshot to GLM-4.5V...")
    result = client.analyze_image(image_data, prompt)
    
    if result and 'content' in result:
        analysis = result['content'][0]['text']
        print("\n✅ Error Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        return True
    else:
        print("❌ Test failed - no response")
        return False


def test_code_screenshot_analysis():
    """Test 3: Code Screenshot Analysis"""
    print("\n" + "="*60)
    print("🎯 TEST 3: Code Screenshot Analysis")
    print("="*60)
    
    client = VisionTestClient()
    
    # Create a code screenshot
    code_img = Image.new('RGB', (800, 500), color='#1e1e1e')
    draw = ImageDraw.Draw(code_img)
    
    code_lines = [
        "def create_session(workflow_id: str):",
        "    try:",
        "        session = client.create_session(",
        "            workflow_id=workflow_id",
        "        )",
        "        return session",
        "    except Exception as e:",
        "        logger.error(f'Session failed: {e}')",
        "        raise HTTPException(500)",
    ]
    
    for i, line in enumerate(code_lines):
        y = 50 + (i * 40)
        # Line numbers
        draw.text((20, y), f"{i+1}", fill='#858585')
        # Code
        draw.text((80, y), line, fill='#d4d4d4')
    
    image_data = client.encode_image(image=code_img)
    
    prompt = """
    Analyze this code screenshot and provide:
    1. What programming language is this?
    2. What does this function do?
    3. Are there any potential bugs or issues?
    4. Suggest improvements for error handling
    5. Rate the code quality (1-10) and explain why
    """
    
    print("\n📤 Sending code screenshot to GLM-4.5V...")
    result = client.analyze_image(image_data, prompt)
    
    if result and 'content' in result:
        analysis = result['content'][0]['text']
        print("\n✅ Code Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        return True
    else:
        print("❌ Test failed - no response")
        return False


def test_architecture_diagram():
    """Test 4: Architecture Diagram Understanding"""
    print("\n" + "="*60)
    print("🎯 TEST 4: Architecture Diagram Analysis")
    print("="*60)
    
    client = VisionTestClient()
    
    # Create architecture diagram
    arch_img = Image.new('RGB', (900, 600), color='white')
    draw = ImageDraw.Draw(arch_img)
    
    # Frontend box
    draw.rectangle([50, 100, 250, 250], fill='#dbeafe', outline='#3b82f6', width=2)
    draw.text((100, 150), "Frontend", fill='#1e40af')
    draw.text((80, 180), "Next.js + React", fill='#1e3a8a')
    
    # Backend box
    draw.rectangle([350, 100, 550, 250], fill='#dcfce7', outline='#22c55e', width=2)
    draw.text((400, 150), "Backend", fill='#166534')
    draw.text((380, 180), "FastAPI + Python", fill='#14532d')
    
    # Database box
    draw.rectangle([650, 100, 850, 250], fill='#fef3c7', outline='#f59e0b', width=2)
    draw.text((700, 150), "Database", fill='#92400e')
    draw.text((690, 180), "PostgreSQL", fill='#78350f')
    
    # Arrows
    draw.line([250, 175, 350, 175], fill='#6b7280', width=3)
    draw.text((280, 155), "API", fill='#4b5563')
    
    draw.line([550, 175, 650, 175], fill='#6b7280', width=3)
    draw.text((580, 155), "SQL", fill='#4b5563')
    
    # Agents box
    draw.rectangle([350, 300, 550, 450], fill='#fce7f3', outline='#ec4899', width=2)
    draw.text((400, 350), "AI Agents", fill='#9f1239')
    draw.text((370, 380), "Multi-Agent System", fill='#831843')
    
    # MCP Tools box
    draw.rectangle([650, 300, 850, 450], fill='#e0e7ff', outline='#6366f1', width=2)
    draw.text((700, 350), "MCP Tools", fill='#3730a3')
    draw.text((670, 380), "CLI, Web, Files", fill='#312e81')
    
    image_data = client.encode_image(image=arch_img)
    
    prompt = """
    Analyze this architecture diagram and explain:
    1. What type of system architecture is shown?
    2. Identify all components and their roles
    3. Describe the data flow between components
    4. What architectural patterns are being used?
    5. Suggest potential improvements or concerns
    """
    
    print("\n📤 Sending architecture diagram to GLM-4.5V...")
    result = client.analyze_image(image_data, prompt)
    
    if result and 'content' in result:
        analysis = result['content'][0]['text']
        print("\n✅ Architecture Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        return True
    else:
        print("❌ Test failed - no response")
        return False


def test_visual_regression():
    """Test 5: Visual Regression Detection"""
    print("\n" + "="*60)
    print("🎯 TEST 5: Visual Regression Detection")
    print("="*60)
    
    client = VisionTestClient()
    
    # Create "before" version
    before_img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(before_img)
    draw.rectangle([50, 50, 350, 250], fill='#3b82f6')
    draw.text((150, 140), "Login Button", fill='white')
    
    # Create "after" version with regression
    after_img = Image.new('RGB', (400, 300), color='white')
    draw2 = ImageDraw.Draw(after_img)
    draw2.rectangle([50, 50, 350, 250], fill='#3b82f6')
    draw2.text((150, 140), "Login Btn", fill='white')  # Text changed
    draw2.rectangle([50, 250, 150, 270], fill='#ef4444')  # Red error indicator
    
    # Combine images side by side
    combined = Image.new('RGB', (850, 300), color='white')
    combined.paste(before_img, (0, 0))
    combined.paste(after_img, (425, 0))
    
    # Add labels
    draw3 = ImageDraw.Draw(combined)
    draw3.text((150, 10), "BEFORE", fill='#10b981')
    draw3.text((575, 10), "AFTER", fill='#ef4444')
    draw3.line([400, 0, 400, 300], fill='#9ca3af', width=2)
    
    image_data = client.encode_image(image=combined)
    
    prompt = """
    Compare these two UI screenshots (BEFORE on left, AFTER on right).
    
    Identify:
    1. What visual differences do you see?
    2. Are these differences intentional improvements or regressions?
    3. Does the button text change affect usability?
    4. What does the red indicator in AFTER version suggest?
    5. Should this change be approved or rejected in a PR review?
    """
    
    print("\n📤 Sending visual comparison to GLM-4.5V...")
    result = client.analyze_image(image_data, prompt)
    
    if result and 'content' in result:
        analysis = result['content'][0]['text']
        print("\n✅ Regression Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        return True
    else:
        print("❌ Test failed - no response")
        return False


def run_all_tests():
    """Run all vision integration tests"""
    print("\n" + "="*60)
    print("🚀 STARTING VISION INTEGRATION TESTS")
    print("="*60)
    print(f"\n📋 Configuration:")
    print(f"   Model: {os.getenv('ANTHROPIC_MODEL')}")
    print(f"   API: {os.getenv('ANTHROPIC_BASE_URL')}")
    print(f"   Auth Token: {os.getenv('ANTHROPIC_AUTH_TOKEN')[:20]}...")
    
    tests = [
        ("UI Component Recognition", test_ui_component_recognition),
        ("Error State Detection", test_error_detection),
        ("Code Screenshot Analysis", test_code_screenshot_analysis),
        ("Architecture Diagram Analysis", test_architecture_diagram),
        ("Visual Regression Detection", test_visual_regression),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "="*60)
    print(f"Overall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 ALL TESTS PASSED! Vision integration working perfectly!")
    else:
        print(f"⚠️  {total_count - passed_count} test(s) failed. Check logs above.")
    
    print("="*60 + "\n")
    
    return passed_count == total_count


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

