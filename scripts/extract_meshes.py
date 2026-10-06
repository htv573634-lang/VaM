import UnityPy
import os

OUT = "out"
os.makedirs(OUT, exist_ok=True)

# Files to extract (place these in vam_assets/)
BUNDLES = {
    "f_1": "vam_assets/f_1",
    "m_1": "vam_assets/m_1",
}

for name, path in BUNDLES.items():
    if not os.path.exists(path):
        print(f"❌ Missing: {path}")
        continue

    print(f"\n{'='*60}")
    print(f"  Extracting: {name} ({os.path.getsize(path)/1024/1024:.1f} MB)")
    print(f"{'='*60}")

    env = UnityPy.load(path)

    # List everything
    for obj in env.objects:
        print(f"  [{obj.type.name}]")

    # Extract meshes
    mesh_count = 0
    for obj in env.objects:
        if obj.type.name == "Mesh":
            mesh = obj.read()
            mesh_count += 1
            print(f"\n  Mesh: {mesh.m_Name}")
            print(f"    Vertices: {len(mesh.m_Vertices) if hasattr(mesh, 'm_Vertices') else '?'}")
            obj_path = f"{OUT}/{name}_{mesh.m_Name}.obj"
            with open(obj_path, "wb") as f:
                f.write(mesh.export())
            print(f"    ✅ Exported: {obj_path}")

    # Extract textures
    tex_count = 0
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            tex = obj.read()
            tex_count += 1
            try:
                img = tex.image
                img_path = f"{OUT}/{name}_{tex.m_Name}.png"
                img.save(img_path)
                print(f"    🖼  Texture: {img_path}")
            except Exception as e:
                print(f"    ⚠️  Texture {tex.m_Name}: {e}")

    # Extract materials
    mat_count = 0
    for obj in env.objects:
        if obj.type.name == "Material":
            mat = obj.read()
            mat_count += 1
            print(f"    🎨 Material: {mat.m_Name}")

    print(f"\n  Summary for {name}: {mesh_count} meshes, {tex_count} textures, {mat_count} materials")

print("\n✅ Extraction complete.")
