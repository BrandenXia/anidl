type OnlyLiteralKeys<T> = string extends keyof T ? never : T;

type BaseProviderOpts = {
  AnimeID: unknown;
  EpID: unknown;
  SearchOpts: object;
  EpOpts: object;
  DownloadOpts: object;
};

type BaseProviderDefaultOpts = {
  AnimeID: string;
  EpID: string;
  SearchOpts: {};
  EpOpts: {};
  DownloadOpts: {};
};

type ResolveProviderOptions<TOverrides extends Partial<BaseProviderOpts>> =
  BaseProviderDefaultOpts & TOverrides;

type BaseProvider<TOverrides extends Partial<BaseProviderOpts> = {}> =
  ResolveProviderOptions<TOverrides> extends infer TOpts
    ? TOpts extends BaseProviderOpts // Safety check on the inferred type
      ? {
          search: (
            query: string,
            opts?: OnlyLiteralKeys<TOpts["SearchOpts"]>,
          ) => Promise<Record<string, TOpts["AnimeID"]>>;
          getEps: (
            id: TOpts["AnimeID"],
            opts?: OnlyLiteralKeys<TOpts["EpOpts"]>,
          ) => Promise<Record<string, TOpts["EpID"]>>;
          download: (
            animeId: TOpts["AnimeID"],
            epId: TOpts["EpID"],
            opts?: OnlyLiteralKeys<TOpts["DownloadOpts"]>,
          ) => Promise<void>;
        }
      : never
    : never;
