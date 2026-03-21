# Mixamo to Godot

Blender addon that prepares Mixamo animations for Godot with root motion support.

## Features

- Batch FBX import with auto-rename to PascalCase
- Adds `mixamorig:Root` bone and transfers horizontal movement from Hips to Root
- Applies transforms and scales location fcurves (cm to meters)
- Merges all animations into one armature, pushes to NLA, cleans up the scene
- One-click "Import + Fix + Merge" button
- Supports Blender 3.x through 5.x (layered actions API)

## Installation

1. Blender → Edit → Preferences → Add-ons → Install
2. Select `mixamo_to_godot.py`, enable it

## Usage

1. Press `N` in 3D View → **Mixamo** tab
2. Set path to folder with FBX files
3. Click **Import + Fix + Merge**

The folder should contain one FBX with a skinned character and the rest as animation-only FBX files. The addon auto-detects which one has the mesh.

## Export

File → Export → glTF 2.0 (.glb) with "NLA Strips" enabled under Animation.

## Godot Setup

1. Import the `.glb` file
2. In your AnimationTree, set `root_motion_track` to `mixamorig_Root` (colon becomes underscore)
3. Set AnimationTree `callback_mode_process` to **Physics** — this is important if your monitor refresh rate differs from physics rate (e.g. 144Hz/210Hz monitor with 60fps physics)

Example root motion code (C#):
```csharp
public override void _PhysicsProcess(double delta) {
    float dt = (float)delta;
    Vector3 velocity = Velocity;

    if (!IsOnFloor())
        velocity.Y -= gravity * dt;

    Quaternion rotation = Transform.Basis.GetRotationQuaternion().Normalized();
    Vector3 rootMotion = rotation * animationTree.GetRootMotionPosition() / dt;

    velocity.X = rootMotion.X;
    velocity.Z = rootMotion.Z;

    Velocity = velocity;
    MoveAndSlide();
}
```

## Compatibility

Blender 3.x / 4.x / 5.x, Godot 4.x

---

# Mixamo to Godot (RU)

Blender-аддон для подготовки анимаций из Mixamo под Godot с поддержкой root motion.

## Возможности

- Пакетный импорт FBX с авто-переименованием в PascalCase
- Добавляет кость `mixamorig:Root` и переносит горизонтальное перемещение с Hips на Root
- Применяет трансформы и масштабирует location-кривые (см в метры)
- Объединяет все анимации в одну арматуру, пушит в NLA, чистит сцену
- Кнопка "Import + Fix + Merge" — всё за один клик
- Поддержка Blender 3.x — 5.x (layered actions API)

## Установка

1. Blender → Edit → Preferences → Add-ons → Install
2. Выбрать `mixamo_to_godot.py`, включить

## Использование

1. В 3D View нажать `N` → вкладка **Mixamo**
2. Указать путь к папке с FBX файлами
3. Нажать **Import + Fix + Merge**

В папке должен быть один FBX с персонажем (со скином) и остальные — только анимации. Аддон сам определяет где меш.

## Экспорт

File → Export → glTF 2.0 (.glb), в настройках включить "NLA Strips" в разделе Animation.

## Настройка в Godot

1. Импортировать `.glb` файл
2. В AnimationTree указать `root_motion_track` = `mixamorig_Root` (двоеточие заменяется на подчёркивание)
3. Выставить `callback_mode_process` у AnimationTree на **Physics** — это важно если частота монитора отличается от физики (например 144Hz/210Hz монитор при 60fps физике)

Пример кода root motion (C#):
```csharp
public override void _PhysicsProcess(double delta) {
    float dt = (float)delta;
    Vector3 velocity = Velocity;

    if (!IsOnFloor())
        velocity.Y -= gravity * dt;

    Quaternion rotation = Transform.Basis.GetRotationQuaternion().Normalized();
    Vector3 rootMotion = rotation * animationTree.GetRootMotionPosition() / dt;

    velocity.X = rootMotion.X;
    velocity.Z = rootMotion.Z;

    Velocity = velocity;
    MoveAndSlide();
}
```

## Совместимость

Blender 3.x / 4.x / 5.x, Godot 4.x
