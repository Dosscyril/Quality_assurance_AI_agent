from playwright.async_api import async_playwright
import asyncio
from backend.agent import get_next_action,explain_report,generate_testcases
async def validate_navigation(page, prev_url):
    if page.url != prev_url:
        return "Navigation successful"
    return "No navigation happened"
async def run_exploration_agent(page,steps=3,goal="explore"):
    findings=[]
    visted=set()
    for step in range(steps):
        screenshot_path=f"agent_step_{step}.png"
        await page.screenshot(path=screenshot_path)

#  FALLBACK EXPLORATION (FORCE ACTIONS)
        # scroll first (bring elements into view)
        await page.mouse.wheel(0, 500)

        buttons = await page.query_selector_all("button")
        links = await page.query_selector_all("a")

        if step == 0 and buttons:
            try:
                if await buttons[0].is_visible():
                    await buttons[0].click(timeout=2000)
                    findings.append("Fallback clicked visible button")
                    continue
                else:
                    findings.append("Fallback button not visible, skipping")
            except Exception as e:
                findings.append(f"Fallback button failed: {str(e)}")

        if step == 1 and links:
            try:
                if await links[0].is_visible():
                    await links[0].click(timeout=2000)
                    findings.append("Fallback clicked visible link")
                    continue
                else:
                    findings.append("Fallback link not visible, skipping")
            except Exception as e:
                findings.append(f"Fallback link failed: {str(e)}")
        if step >= 2:
            await page.mouse.wheel(0, 800)
            findings.append("Fallback scroll to explore page")

# AI decision
        dom = await extract_dom_summary(page)
        action = get_next_action(screenshot_path, dom,goal)
        if not action:
            findings.append("AI failed, continuing exploration...")
            continue
        if "type" not in action:
            findings.append("invalid action format from ai")
            continue
        action_key=f"{action['type']}:{action.get('selector','')}"
        if action_key in visted:
            findings.append(f"skipped repeated action:{action_key}")
            continue
        visted.add(action_key)
        max_retries=2
        for attempt in range(max_retries):
            try:
                if action["type"]=="click":
                    if "selector" not in action:
                        findings.append("missing selector")
                        break
                    prev_url = page.url
                    msg = await resolve_and_click(page, action["selector"])
                    findings.append(msg)
                    await page.wait_for_timeout(2000)
                    validation = await validate_goal(page, goal)
                    if "successful" in validation.lower():
                        findings.append(validation)
                        return findings
                    break
                elif action["type"]=="fill":
                    if "selector" not in action:
                        findings.append("missing selector")
                        break
                    msg = await resolve_and_fill(page, action["selector"], "test")
                    findings.append(msg)
                    findings.append("Input field tested")
                    break
                elif action["type"]=="wait":
                    await page.wait_for_timeout(2000)
                    findings.append("waited")
                    break
                elif action["type"]=="done":
                    findings.append("AI suggested done, but continuing exploration...")
                    break
                elif action["type"] == "scroll":
                    await page.mouse.wheel(0, 500)
                    findings.append("Scrolled down")
                    break
            except Exception as e:
                findings.append(f"retry{attempt+1}failed:{str(e)}")
                await asyncio.sleep(1)
    findings.append("max steps reached")
    return findings
    
async def run_agent(url: str, max_steps: int = 5,goal: str="explore"):
    from playwright.async_api import async_playwright
    import time

    report = []
    score = 100

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        try:
            start = time.time()
            await page.goto(url, timeout=10000)
            end = time.time()
            load_time = end - start

            report.append({"type": "success", "message": "Page loaded successfully"})

            if load_time > 5:
                report.append({"type": "warning", "message": f"Slow load time: {load_time:.2f}s"})
                score -= 10
            else:
                report.append({"type": "success", "message": f"Load time: {load_time:.2f}s"})

        except:
            report.append({"type": "error", "message": "Page failed to load"})
            return {"status": "failed", "score": 0, "report": report}

        #Title Check
        title = await page.title()
        if title:
            report.append({"type": "success", "message": f"Page title: {title}"})
        else:
            report.append({"type": "warning", "message": "Page has no title"})
            score -= 10

        #Buttons Check
        buttons = await page.query_selector_all("button")
        if buttons:
            report.append({"type": "success", "message": f"{len(buttons)} buttons found"})
        else:
            report.append({"type": "warning", "message": "No buttons found"})
            score -= 10

        # Input Fields Check
        inputs = await page.query_selector_all("input")
        if inputs:
            report.append({"type": "success", "message": f"{len(inputs)} input fields found"})
        else:
            report.append({"type": "warning", "message": "No input fields found"})
            score -= 10

        # Links Check
        links = await page.query_selector_all("a")
        if links:
            report.append({"type": "success", "message": f"{len(links)} links found"})
        else:
            report.append({"type": "warning", "message": "No links found"})
            score -= 10

        # Broken Links Detection
        broken_links = 0
        for a in links[:5]:  # limit for speed
            href = await a.get_attribute("href")
            if href and href.startswith("http"):
                try:
                    resp = await page.request.get(href)
                    if resp.status >= 400:
                        broken_links += 1
                except:
                    broken_links += 1

        if broken_links > 0:
            report.append({"type": "error", "message": f"{broken_links} broken links found"})
            score -= 15
        else:
            report.append({"type": "success", "message": "No broken links detected"})

        # Empty Page Detection
        content = await page.content()
        if len(content.strip()) < 200:
            report.append({"type": "error", "message": "Page content too small (possible blank page)"})
            score -= 20

        # Heading Check
        headings = await page.query_selector_all("h1, h2, h3")
        if not headings:
            report.append({"type": "warning", "message": "No headings found"})
            score -= 5
        else:
            report.append({"type": "success", "message": f"{len(headings)} headings found"})

        # Screenshot
        await page.screenshot(path="backend/static/final.png")

        # Agent
        agent_findings = await run_exploration_agent(page, steps=10,goal=goal)

        await browser.close()
        explanation = explain_report(report)
        testcases = generate_testcases(report)
    return{
        "status":"completed",
        "score":score,
        "report":report,
        "agent_findings":agent_findings,
        "ai_explanation":explanation,
        "testcases":testcases
    }
async def extract_dom_summary(page):
    elements=[]
    buttons=await page.query_selector_all("button")
    for b in buttons[:5]:
        text=await b.inner_text()
        elements.append({"type":"button","text":text.strip()})
    inputs=await page.query_selector_all("input")
    for i in inputs[:5]:
        name=await i.get_attribute("name")
        placeholder=await i.get_attribute("placeholder")
        elements.append({
            "type":"input",
            "name":name,
            "placeholder":placeholder
        })
    links=await page.query_selector_all("a")
    for l in links[:5]:
        text=await l.inner_text()
        elements.append({"type":"link","text":text.strip()})
    return elements
async def resolve_and_click(page, selector):
    try:
        await page.click(selector, timeout=2000)
        return f"clicked:{selector}"
    except:
        pass

    text = selector.replace("text=", "").strip().lower()

    try:
        candidates = await page.query_selector_all("button,a")

        # 🔥 SMART MATCH
        priority_words = ["login", "sign in", "submit", "search", "next"]

        for word in priority_words:
            for c in candidates[:15]:
                t = (await c.inner_text()).strip().lower()
                if word in t:
                    await c.click()
                    return f"clicked smart match:{word}"

        # fallback
        for c in candidates[:10]:
            t = (await c.inner_text()).strip().lower()
            if text in t:
                await c.click()
                return f"clicked via text match:{text}"

    except:
        pass

    return f"failed to click:{selector}"
async def resolve_and_fill(page, selector, value="test"):
    try:
        await page.fill(selector, value, timeout=2000)
        return f"Filled: {selector}"
    except:
        pass
    inputs = await page.query_selector_all("input")
    for i in inputs[:5]:
        try:
            await i.fill(value)
            return "Filled via fallback input"
        except:
            continue

    return f"Failed to fill: {selector}"
async def validate_goal(page, goal):
    goal = goal.lower()

    if "login" in goal:
        if "dashboard" in page.url or "home" in page.url:
            return "Login successful"
        return "Login failed"

    if "search" in goal:
        content = await page.content()
        if "result" in content.lower():
            return "Search results found"
        return "Search failed"

    return "No goal validation"