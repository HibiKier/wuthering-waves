# 鸣潮数据模型设计

## 角色与相关数据的关联关系

### 角色 (WavesCharacter)

角色是核心实体，包含角色的基本信息，如 ID、名称、等级、属性等。

### 技能 (Skill)

技能是可以被多个角色共享的实体，包含技能 ID、名称、描述等信息。

- 一个角色可以拥有多个技能
- 一个技能可以被多个角色使用
- 使用`WavesCharSkill`关联表存储角色与技能的多对多关系，同时记录技能等级

### 链 (Chain)

链是可以被多个角色共享的实体，包含链的名称、顺序、描述等信息。

- 一个角色可以拥有多个链
- 一个链可以被多个角色使用
- 使用`WavesCharChain`关联表存储角色与链的多对多关系

### 武器 (Weapon)

武器与角色是一对一关系，每个角色只能装备一个武器。

- 一个角色只能拥有一个武器
- 武器详情(`WeaponDetail`)可以被多个角色共享
- 使用`Weapon`表存储角色与武器的一对一关系，包含武器等级、突破等级等信息

### 声骇装备 (Phantom)

声骇装备与角色是一对多关系，每个角色最多可以装备 5 个声骇装备。

- 一个角色可以拥有多个声骇装备（最多 5 个）
- 使用`Phantom`表存储角色与声骇装备的一对多关系
- 声骇装备的属性通过`PhantomProps`表与`Props`表关联

## 数据模型关系图

```
WavesCharacter
 |
 |-- WavesCharSkill -- Skill
 |
 |-- WavesCharChain -- Chain
 |
 |-- Weapon -- WeaponDetail
 |
 |-- Phantom -- FetterDetail
      |
      |-- PhantomProps -- Props
```

## 数据获取流程

1. 通过 API 获取角色详情数据(CharDetailData)
2. 保存角色基本信息到 WavesCharacter 表
3. 保存技能信息到 Skill 表，并建立 WavesCharacter 与 Skill 的关联(WavesCharSkill)
4. 保存链信息到 Chain 表，并建立 WavesCharacter 与 Chain 的关联(WavesCharChain)
5. 保存武器信息到 WeaponDetail 表，并建立 WavesCharacter 与 WeaponDetail 的关联(Weapon)
6. 保存声骇装备信息到 Phantom 表，并建立 WavesCharacter 与 Phantom 的关联

## 数据查询方法

- `WavesCharHandler.get_char_skills(char_id)`: 获取角色的技能列表及等级
- `WavesCharHandler.get_char_chains(char_id)`: 获取角色的链列表
- 角色的武器可通过`character.weapon`关联获取
- 角色的声骇装备可通过`character.phantoms`关联获取
