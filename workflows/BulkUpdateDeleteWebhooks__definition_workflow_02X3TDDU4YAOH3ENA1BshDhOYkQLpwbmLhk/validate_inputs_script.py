"""Source for Validate Workflow Inputs — paste target is workflow JSON activity."""
SCRIPT = '''"""
Validate Workflow Inputs — consolidated preflight checks.

  argv[1]  Operation
  argv[2]  Target Type
  argv[3]  Webhook URL
  argv[4]  Webhook Name
  argv[5]  Webhook Secret (not validated; reserved)
  argv[6]  Local - Operation Keyword Delete
  argv[7]  Local - Operation Keyword Update
  argv[8]  Local - Target Type Keyword Networks
  argv[9]  Local - Target Type Keyword Templates

Script queries: validation_failed, error_message, final_report, output_result
"""

import json
import re
import sys

HTTPS_URL_RE = re.compile(r"^https://[^\s/$.?#][^\s]*$")


def arg(n, default=""):
    return sys.argv[n].strip() if len(sys.argv) > n else default


operation = arg(1)
target_type = arg(2)
webhook_url = arg(3)
webhook_name = arg(4)
# argv[5] Webhook Secret — intentionally not validated here
kw_delete = arg(6)
kw_update = arg(7)
kw_networks = arg(8)
kw_templates = arg(9)

errors = []

if operation != kw_update and operation != kw_delete:
    errors.append(
        "Invalid operation. Use " + kw_update + " or " + kw_delete + "."
    )

if target_type != kw_networks and target_type != kw_templates:
    errors.append(
        "Invalid target type. Use "
        + kw_networks
        + " or "
        + kw_templates
        + "."
    )

if not webhook_url:
    errors.append("Webhook URL is required.")
elif not HTTPS_URL_RE.match(webhook_url):
    errors.append("Webhook URL must be a valid HTTPS URL (https://...).")

if operation == kw_update and not webhook_name:
    errors.append(
        'Webhook Name is required when Operation is "' + kw_update + '".'
    )

if operation == kw_delete and webhook_name:
    errors.append(
        'Webhook Name must be empty when Operation is "' + kw_delete + '".'
    )

if operation == kw_delete and arg(5):
    errors.append(
        'Webhook Secret must be empty when Operation is "' + kw_delete + '".'
    )

validation_failed = bool(errors)
if len(errors) == 1:
    error_message = errors[0]
else:
    error_message = "; ".join(errors)

final_report = ""
output_result = ""

if validation_failed:
    lines = ["Input validation failed", ""]
    for item in errors:
        lines.append("- " + item)
    final_report = chr(10).join(lines)
    output_result = json.dumps(
        {
            "status": "Failed",
            "statusCode": "400",
            "validationErrors": errors,
            "errorMessage": error_message,
            "targets": [],
        },
        separators=(",", ":"),
    )
'''

if __name__ == "__main__":
    import json
    from pathlib import Path

    path = Path(__file__).with_name(
        "definition_workflow_02X3TDDU4YAOH3ENA1BshDhOYkQLpwbmLhk.json"
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    act_id = "definition_activity_02X9TANLH2G7D78TILbPkQFBpTRT8sPE1np"

    def walk(o):
        if isinstance(o, dict) and o.get("unique_name") == act_id:
            p = o["properties"]
            p["script"] = SCRIPT
            o["name"] = "Execute Python Script"
            o["title"] = "Validate Workflow Inputs"
            p["display_name"] = "Validate Workflow Inputs"
            p["description"] = (
                "Validate Operation, Target Type, Webhook URL, and Webhook Name "
                "before organization lookup."
            )
            return True
        if isinstance(o, dict):
            for v in o.values():
                if walk(v):
                    return True
        elif isinstance(o, list):
            for i in o:
                if walk(i):
                    return True
        return False

    if not walk(data):
        raise SystemExit("activity not found")

    bad = "$activity.definition_activity_02X9TANLH2G7D78TILbPkQFBpTRT8sPE1np.output.error.message$"
    good = "$activity.definition_activity_02X9TANLH2G7D78TILbPkQFBpTRT8sPE1np.output.script_queries.error_message$"

    def fix_refs(o):
        if isinstance(o, dict):
            if o.get("variable_value_new") == bad:
                o["variable_value_new"] = good
            for v in o.values():
                fix_refs(v)
        elif isinstance(o, list):
            for i in o:
                fix_refs(i)

    fix_refs(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("OK")
