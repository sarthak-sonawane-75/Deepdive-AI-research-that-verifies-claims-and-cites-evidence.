from app.core.mesh import mesh_chat

try:
    response = mesh_chat(
        system_prompt="You are a helpful assistant.",
        user_prompt="Reply with exactly: DeepDive connection successful.",
        temperature=0,
    )
    print("SUCCESS!")
    print(response)

except Exception as e:
    print("CONNECTION FAILED")
    print(f"{type(e).__name__}: {e}")