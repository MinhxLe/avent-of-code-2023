def edit_distance(s1: str, s2: str) -> int:
    assert len(s1) == len(s2)
    return sum([a != b for a, b in zip(s1, s2)])


def is_horizonal_reflection(image: list[str], axis: int, smudge_count: int = 0):
    """
    we define axis as the line between axis and axis+1
    """
    M = len(image)
    # we do not allow axis of reflection to be boundaries
    assert 0 <= axis < M
    for i in range(0, axis + 1):
        dist_from_axis = axis - i
        reflected_i = axis + dist_from_axis + 1
        if reflected_i < M:
            dist = edit_distance(image[i], image[reflected_i])
            smudge_count -= dist
            if smudge_count < 0:
                return False
    return smudge_count == 0


def is_vertical_reflection(image: list[str], axis: int):
    """
    we define axis as the line between axis and axis+1
    """
    new_image = transpose(image)
    return is_horizonal_reflection(new_image, axis)


def transpose(image: list[str]) -> list[str]:
    M, N = len(image), len(image[0])

    new_image = []
    for j in range(N):
        new_row = ""
        for i in range(M):
            new_row += image[i][j]
        new_image.append(new_row)
    return new_image


def summarize_image(image: list[str], smudge_count: int = 0):
    M, N = len(image), len(image[0])
    horizonal_lines = []
    for i in range(0, M - 1):
        if is_horizonal_reflection(image, i, smudge_count):
            horizonal_lines.append(i)
    vertical_lines = []
    image_transposed = transpose(image)
    for i in range(0, N - 1):
        if is_horizonal_reflection(image_transposed, i, smudge_count):
            vertical_lines.append(i)
    return horizonal_lines, vertical_lines


def calculate_score(horizonal_lines, vertical_lines):
    return sum([(v + 1) for v in vertical_lines]) + sum(
        [(h + 1) * 100 for h in horizonal_lines]
    )


def summarize_images(images: list[list[str]], smudge_count: int = 0) -> int:
    total = 0
    for image in images:
        horizonal_lines, vertical_lines = summarize_image(image, smudge_count)
        total += calculate_score(horizonal_lines, vertical_lines)
    return total


with open("./reflection_13.txt") as f:
    lines = [line.rstrip() for line in f]
images = []
image = []
for line in lines:
    if line == "":
        images.append(image)
        image = []
    else:
        image.append(line)
if image:
    images.append(image)

# part 1
print(summarize_images(images))

# part2
summaries1 = [summarize_image(i) for i in images]
summaries2 = [summarize_image(i, 1) for i in images]

new_score = 0
for old, new in zip(summaries1, summaries2):
    old_hl, old_vl = old
    new_hl, new_vl = new
    hl = list(set(new_hl) - set(old_hl))
    vl = list(set(new_vl) - set(old_vl))
    new_score += calculate_score(hl, vl)
print(new_score)
