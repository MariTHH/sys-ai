% Факты с одним аргументом (описание классов ролей героев)
role(tank).        % Герой с ролью "Танк"
role(fighter).     % Герой с ролью "Боец"
role(marksman).    % Герой с ролью "Стрелок"
role(mage).        % Герой с ролью "Маг"
role(support).     % Герой с ролью "Поддержка"
role(assassin).    % Герой с ролью "Убийца"

% Факты о героях (список героев в игре)
hero(alucard).     % Герой "Alucard"
hero(lesley).      % Герой "Lesley"
hero(gord).        % Герой "Gord"
hero(rafaela).     % Герой "Rafaela"
hero(miya).        % Герой "Miya"
hero(balmond).     % Герой "Balmond"
hero(franco).      % Герой "Franco"
hero(aurora).      % Герой "Aurora"
hero(lancelot).    % Герой "Lancelot"
hero(karrie).      % Герой "Karrie"
hero(granger).     % Герой "Granger"
hero(harley).      % Герой "Harley"
hero(saber).       % Герой "Saber"
hero(clint).       % Герой "Clint"
hero(zhask).       % Герой "Zhask"
hero(tigreal).     % Герой "Tigreal"
hero(chou).        % Герой "Chou"
hero(fanny).       % Герой "Fanny"
hero(hayabusa).    % Герой "Hayabusa"
hero(gusion).      % Герой "Gusion"

% Факты о ролях героев (герой и его роль)
has_role(alucard, fighter).       % Alucard — Боец
has_role(lesley, marksman).       % Lesley — Стрелок
has_role(gord, mage).             % Gord — Маг
has_role(rafaela, support).       % Rafaela — Поддержка
has_role(miya, marksman).         % Miya — Стрелок
has_role(balmond, tank).          % Balmond — Танк
has_role(franco, tank).           % Franco — Танк
has_role(aurora, mage).           % Aurora — Маг
has_role(lancelot, assassin).     % Lancelot — Убийца
has_role(karrie, marksman).       % Karrie — Стрелок
has_role(granger, marksman).      % Granger — Стрелок
has_role(harley, assassin).       % Harley — Убийца
has_role(saber, assassin).        % Saber — Убийца
has_role(clint, marksman).        % Clint — Стрелок
has_role(zhask, mage).            % Zhask — Маг
has_role(tigreal, tank).          % Tigreal — Танк
has_role(chou, fighter).          % Chou — Боец
has_role(fanny, assassin).        % Fanny — Убийца
has_role(hayabusa, assassin).     % Hayabusa — Убийца
has_role(gusion, assassin).       % Gusion — Убийца

% Факты о фракциях героев (герой и его фракция)
has_faction(alucard, moniyan).      % Alucard принадлежит к фракции Moniyan
has_faction(lesley, empire).        % Lesley принадлежит к фракции Empire
has_faction(gord, celestial).       % Gord принадлежит к фракции Celestial
has_faction(rafaela, celestial).    % Rafaela принадлежит к фракции Celestial
has_faction(miya, elf).             % Miya принадлежит к фракции Elf
has_faction(balmond, orc).          % Balmond принадлежит к фракции Orc
has_faction(franco, north_valley).  % Franco принадлежит к фракции North Valley
has_faction(aurora, northern_veil). % Aurora принадлежит к фракции Northern Veil
has_faction(lancelot, empire).      % Lancelot принадлежит к фракции Empire
has_faction(karrie, yan_valley).    % Karrie принадлежит к фракции Yan Valley
has_faction(granger, empire).       % Granger принадлежит к фракции Empire
has_faction(harley, magic_academy). % Harley принадлежит к фракции Magic Academy
has_faction(saber, empire).         % Saber принадлежит к фракции Empire
has_faction(clint, wild_west).      % Clint принадлежит к фракции Wild West
has_faction(zhask, alien_invasion). % Zhask принадлежит к фракции Alien Invasion
has_faction(tigreal, moniyan).      % Tigreal принадлежит к фракции Moniyan
has_faction(chou, eastern_village). % Chou принадлежит к фракции Eastern Village
has_faction(fanny, empire).         % Fanny принадлежит к фракции Empire
has_faction(hayabusa, shadow).      % Hayabusa принадлежит к фракции Shadow
has_faction(gusion, empire).        % Gusion принадлежит к фракции Empire

% Связи героев (союзники и враги)
ally(alucard, tigreal).     % Alucard и Tigreal — союзники
ally(lancelot, fanny).      % Lancelot и Fanny — союзники
ally(lesley, granger).      % Lesley и Granger — союзники
ally(hayabusa, gusion).     % Hayabusa и Gusion — союзники
ally(miya, rafaela).        % Miya и Rafaela — союзники

enemy(alucard, balmond).    % Alucard и Balmond — враги
enemy(lancelot, saber).     % Lancelot и Saber — враги
enemy(aurora, zhask).       % Aurora и Zhask — враги
enemy(granger, harley).     % Granger и Harley — враги
enemy(lesley, clint).       % Lesley и Clint — враги

% Правила для нахождения союзников и врагов по ролям

% Правило enemy_role(X, Y) выводит, что два героя являются врагами, если они враги
% (есть факт enemy(X, Y)) и у них разные роли.
enemy_role(X, Y) :- enemy(X, Y), has_role(X, RoleX), has_role(Y, RoleY), RoleX \= RoleY.

% Правило is_ally(X, Y) проверяет, являются ли два героя союзниками.
% Оно проверяет оба направления союза: ally(X, Y) и ally(Y, X).
is_ally(X, Y) :- ally(X, Y); ally(Y, X).

% Правило is_enemy(X, Y) проверяет, являются ли два героя врагами.
% Оно проверяет оба направления вражды: enemy(X, Y) и enemy(Y, X).
is_enemy(X, Y) :- enemy(X, Y); enemy(Y, X).

% Правило find_fighter_allies(X, Y) находит всех союзников героя X, если он имеет роль fighter.
find_fighter_allies(X, Y) :- has_role(X, fighter), is_ally(X, Y).

% Правило find_marksman_enemy(X, Y) находит всех врагов героя X, если он имеет роль marksman.
find_marksman_enemy(X, Y) :- has_role(X, marksman), is_enemy(X, Y).
